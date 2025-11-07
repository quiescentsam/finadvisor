from pipelines.run_rag import main

def test_rag_pipeline_runs(capfd):
    main()
    out, _ = capfd.readouterr()
    assert "RAG pipeline initialized" in out
