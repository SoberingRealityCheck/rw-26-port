package net.shiroha233.roadweaver.pathfinding.cache;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.levelgen.DensityFunction;
import net.minecraft.world.level.levelgen.RandomState;

import java.util.concurrent.ConcurrentHashMap;

/**
 * 快速高度采样器
 *
 * Port note (26.2): the router no longer has initialDensityWithoutJaggedness. It has
 * preliminarySurfaceLevel, a find_top_surface density that returns the surface y directly
 * (multiples of its cell height, 8 in vanilla). Before, this class scanned downward itself and
 * stopped at density > 0.390625, a vanilla-only constant. Now the datapack (Terralith, Tectonic)
 * defines where "surface" is, which is closer to what chunk generation uses.
 */
public final class FastHeightSampler {

    private final DensityFunction preliminarySurfaceLevel;
    private ConcurrentHashMap<Long, Integer> heightCache = new ConcurrentHashMap<>();

    private FastHeightSampler(DensityFunction preliminarySurfaceLevel) {
        this.preliminarySurfaceLevel = preliminarySurfaceLevel;
    }

    public static FastHeightSampler create(ServerLevel level) {
        RandomState randomState = level.getChunkSource().getGeneratorState().randomState();
        return new FastHeightSampler(randomState.router().preliminarySurfaceLevel());
    }

    public int sampleHeight(int x, int z) {
        int alignedX = (x >> 2) << 2;
        int alignedZ = (z >> 2) << 2;
        long key = packXZ(alignedX, alignedZ);
        Integer cached = heightCache.get(key);
        if (cached != null) return cached;

        int height = computeHeight(alignedX, alignedZ);
        heightCache.put(key, height);
        return height;
    }

    public void prewarmRegion(int minX, int minZ, int maxX, int maxZ, int step) {
        for (int x = minX; x <= maxX; x += step) {
            for (int z = minZ; z <= maxZ; z += step) {
                sampleHeight((x >> 2) << 2, (z >> 2) << 2);
            }
        }
    }

    private int computeHeight(int x, int z) {
        // y is ignored by find_top_surface, it scans from its own upper bound
        return (int) preliminarySurfaceLevel.compute(new DensityFunction.SinglePointContext(x, 0, z));
    }

    private static long packXZ(int x, int z) {
        return ((long) x << 32) | (z & 0xFFFFFFFFL);
    }

    /**
     * 释放缓存。用新实例替换而非 clear()，确保内部 table 数组被 GC 回收。
     */
    public void clearCache() {
        heightCache = new ConcurrentHashMap<>();
    }

    public int getCacheSize() {
        return heightCache.size();
    }
}
