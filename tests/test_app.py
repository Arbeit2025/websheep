import importlib
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def make_client():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    os.environ["WEBSHEEP_DB_PATH"] = tmp.name
    import app as app_module

    importlib.reload(app_module)
    app_module.app.config.update(TESTING=True)
    return app_module, app_module.app.test_client()


def test_index_ok_and_mascot_present():
    _, client = make_client()
    res = client.get("/")
    assert res.status_code == 200
    body = res.get_data(as_text=True)
    assert "websheep" in body
    assert 'id="mascot"' in body
    assert 'id="bubble"' in body
    assert 'id="callBtn"' in body
    assert 'id="walkBtn"' in body
    assert 'id="sitBtn"' in body


def test_sheep_svg_present():
    _, client = make_client()
    body = client.get("/").get_data(as_text=True)
    assert 'id="sheepSvg"' in body
    assert 'class="leg leg-a"' in body
    assert 'class="eye"' in body
    assert "charImg" not in body
    assert "cocoa.png" not in body


def test_lines_are_24_and_unique():
    app_module, client = make_client()
    assert len(app_module.SHEEP_LINES) == 24
    assert len(set(app_module.SHEEP_LINES)) == 24
    body = client.get("/").get_data(as_text=True)
    for sample in ["めぇ〜。呼んだ？", "眠れない夜は、わたしを数えてね。", "毛刈りの季節？"]:
        assert sample in body
    # cocoweb（ココア）のセリフ流用でないこと
    assert "私は見ています。" not in body


def test_no_escaped_quotes_in_html():
    # {{ css|safe }} / {{ script|safe }} が効いて、引用符がHTMLエスケープされていないこと
    _, client = make_client()
    body = client.get("/").get_data(as_text=True)
    assert "&#39;" not in body
    assert "&#34;" not in body
    assert 'getElementById("stage")' in body
    assert 'addEventListener("click", callSheep)' in body
    assert "requestAnimationFrame" in body
    assert "pointerdown" in body


def test_no_horizontal_scroll_guard():
    _, client = make_client()
    body = client.get("/").get_data(as_text=True)
    assert "overflow-x:hidden" in body


def test_count_increments():
    _, client = make_client()
    r1 = client.post("/count").get_json()
    r2 = client.post("/count").get_json()
    assert r1["total"] == 1 and r1["today"] == 1
    assert r2["total"] == 2 and r2["today"] == 2


def test_greetings_present():
    _, client = make_client()
    body = client.get("/").get_data(as_text=True)
    assert "おはよう、めぇ〜。今日も牧場は平和だよ。" in body
    assert "羊を数えて、ゆっくり休んでね。" in body


def test_healthz():
    _, client = make_client()
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.get_json() == {"ok": True}


def test_standalone_prototype_exists():
    path = os.path.join(os.path.dirname(__file__), "..", "websheep-prototype.html")
    assert os.path.exists(path)
    with open(path, encoding="utf-8") as f:
        body = f.read()
    assert 'id="sheepSvg"' in body
    assert "めぇ〜。呼んだ？" in body
    assert "&#39;" not in body and "&#34;" not in body
