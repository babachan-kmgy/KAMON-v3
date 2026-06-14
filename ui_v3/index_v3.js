// 検索ボタン・Enter キーのハンドラ設定
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("queryInput");
    const button = document.getElementById("searchButton");

    button.addEventListener("click", () => {
        const q = input.value.trim();
        if (!q) return;
        searchSurname(q);
    });

    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            const q = input.value.trim();
            if (!q) return;
            searchSurname(q);
        }
    });
});

// 通常の姓検索（既存 API を想定）
async function searchSurname(query) {
    const status = document.getElementById("status");
    const list = document.getElementById("results");

    status.textContent = "検索中…";
    list.innerHTML = "";
    hideRagDescription();

    try {
        const res = await fetch(`/api_v3/search?query=${encodeURIComponent(query)}`);
        const data = await res.json();

        if (!Array.isArray(data) || data.length === 0) {
            status.textContent = "該当する姓が見つかりませんでした。";
            return;
        }

        renderResults(data);
        status.textContent = `${data.length} 件ヒットしました。`;

        // RAG 説明文を取得
        fetchRagDescription(query);

    } catch (e) {
        console.error(e);
        status.textContent = "検索 API に接続できませんでした。";
    }
}

// 検索結果の描画（簡易版）
function renderResults(items) {
    const list = document.getElementById("results");
    list.innerHTML = "";

    items.forEach(item => {
        const li = document.createElement("li");

        const kanji = document.createElement("div");
        kanji.className = "kanji";
        kanji.textContent = item.canonical_kanji || item.kanji || "";

        const yomi = document.createElement("div");
        yomi.className = "yomi";
        yomi.textContent = item.canonical_yomi || item.yomi || "";

        const romaji = document.createElement("div");
        romaji.className = "romaji";
        romaji.textContent = item.canonical_romaji || item.romaji || "";

        li.appendChild(kanji);
        li.appendChild(yomi);
        li.appendChild(romaji);

        list.appendChild(li);
    });
}

// RAG 説明文取得
async function fetchRagDescription(query) {
    const box = document.getElementById("ragDescription");
    box.classList.add("hidden");
    box.textContent = "";

    try {
        const res = await fetch(`/api_v3/rag?query=${encodeURIComponent(query)}`);
        const data = await res.json();

        if (data.error) {
            box.textContent = "説明文を取得できませんでした。";
            box.classList.remove("hidden");
            return;
        }

        box.innerHTML = `
            <strong>説明：</strong><br>
            ${escapeHtml(data.description)}
        `;
        box.classList.remove("hidden");

    } catch (e) {
        console.error(e);
        box.textContent = "RAG API に接続できませんでした。";
        box.classList.remove("hidden");
    }
}

function hideRagDescription() {
    const box = document.getElementById("ragDescription");
    box.classList.add("hidden");
    box.textContent = "";
}

// 簡易エスケープ
function escapeHtml(str) {
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}
