/* 文件职责：选择精确高度采样后端。服务端移植版只保留 CPU。 */
package net.shiroha233.roadweaver.pathfinding.cache;

import net.minecraft.server.level.ServerLevel;

/**
 * 精确高度后端工厂。
 * Port note: the OpenCL backend was removed on purpose (CPU-only server). Always CPU.
 */
public final class AccurateHeightBackends {
    private AccurateHeightBackends() {}

    public static AccurateHeightBackend create(ServerLevel level, CpuAccurateHeightBackend cpu) {
        return cpu;
    }
}
