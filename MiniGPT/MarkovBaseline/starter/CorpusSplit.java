import java.util.List;

public record CorpusSplit(
        List<List<Integer>> training,
        List<List<Integer>> validation,
        List<List<Integer>> test) {}