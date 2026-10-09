package net.shiroha233.roadweaver.pathfinding.cache;

import net.minecraft.server.level.ServerLevel;
import net.shiroha233.roadweaver.generation.progress.InitialGenerationProgressTracker;

/**
 * 粗高度批量采样器入口。
 * Port note: OpenCL removed on purpose (CPU-only server). Always CPU.
 */
public final class CoarseHeightBatchSamplers {
    private CoarseHeightBatchSamplers() {}

    public static CoarseHeightBatchSampler create(ServerLevel level, CoarseHeightBatchRequest request) {
        InitialGenerationProgressTracker.setBackend("CPU", "CPU", null);
        return CpuCoarseHeightBatchSampler.create(level);
    }
}
