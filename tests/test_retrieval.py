from rag_nr.retrieval import reciprocal_rank_fusion


def test_rrf_combines_and_ranks():
    fts = [{"id": 1}, {"id": 2}, {"id": 3}]
    dense = [{"id": 2}, {"id": 3}, {"id": 1}]
    fused = reciprocal_rank_fusion([fts, dense])
    fused_ids = [r["id"] for r in fused]
    assert set(fused_ids) == {1, 2, 3}
    # id 2 is top-1 in dense and top-2 in fts — should rank at least as well as id 1.
    assert fused_ids.index(2) <= fused_ids.index(1)


def test_rrf_includes_results_only_in_one_list():
    fts = [{"id": 1}]
    dense = [{"id": 2}]
    fused = reciprocal_rank_fusion([fts, dense])
    assert {r["id"] for r in fused} == {1, 2}


def test_rrf_empty_lists():
    assert reciprocal_rank_fusion([[], []]) == []
