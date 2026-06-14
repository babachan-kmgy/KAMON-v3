document.addEventListener("DOMContentLoaded", () => {

    console.log("KAMON v3 UI loaded.");

    const input = document.getElementById("surnameInput");
    const button = document.getElementById("searchButton");
    const resultArea = document.getElementById("resultArea");

    if (!input || !button || !resultArea) {
        console.error("DOM 要素が見つかりません。ID を確認してください。");
        return;
    }

    // ★ API の URL（開発中はローカルでOK）
    // GitHub Pages からローカル API は直接呼べないので、
    // ローカルで UI を開く場合は http://127.0.0.1:8001 などを使う。
    const API_BASE = "http://127.0.0.1:8000";

    button.addEventListener("click", async () => {
        const q = input.value.trim();
        if (!q) {
            resultArea.innerHTML = "姓を入力してください。";
            return;
        }

        resultArea.innerHTML = "検索中…";

        try {
            const url = `${API_BASE}/search?surname=${encodeURIComponent(q)}`;
            console.log("API request:", url);

            const res = await fetch(url);

            if (!res.ok) {
                throw new Error(`API error: ${res.status}`);
            }

            const data = await res.json();

            resultArea.innerHTML = `
                <h2>検索結果</h2>
                <pre>${JSON.stringify(data, null, 2)}</pre>
            `;
        } catch (err) {
            console.error("API 接続エラー:", err);
            resultArea.innerHTML = `
                <span style="color:red;">API に接続できませんでした。</span><br>
                ローカル API が起動しているか確認してください。
            `;
        }
    });

});
