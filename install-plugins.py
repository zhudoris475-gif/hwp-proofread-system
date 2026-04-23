import os
import json
import urllib.request

BASE = r"C:\Users\doris\Documents\nootbook"
PLUGINS_DIR = os.path.join(BASE, ".obsidian", "plugins")

PLUGINS = [
    {
        "id": "chess-study",
        "repo": "chrislicodes/obsidian-chess-study",
        "name": "Chess Study",
    },
    {
        "id": "chesser-obsidian",
        "repo": "SilentVoid13/Chesser",
        "name": "Chesser",
    },
    {
        "id": "obsidian-chessboard",
        "repo": "THeK3nger/obsidian-chessboard",
        "name": "Chessboard Viewer",
    },
    {
        "id": "translate",
        "repo": "Fevol/obsidian-translate",
        "name": "Translate",
    },
    {
        "id": "obsidian-image-toolkit",
        "repo": "obsidian-community/obsidian-image-toolkit",
        "name": "Image Toolkit",
    },
]

FILES_TO_DOWNLOAD = ["main.js", "manifest.json", "styles.css"]


def download_file(url, dest_path):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(dest_path, "wb") as f:
                f.write(response.read())
        return True
    except Exception as e:
        if "404" in str(e) or "Not Found" in str(e):
            return False
        print(f"    다운로드 실패: {e}")
        return False


def get_latest_release_url(repo, filename):
    return f"https://github.com/{repo}/releases/latest/download/{filename}"


def main():
    print("=" * 50)
    print("  Obsidian 플러그인 자동 설치")
    print("=" * 50)

    os.makedirs(PLUGINS_DIR, exist_ok=True)

    installed = []
    failed = []

    for i, plugin in enumerate(PLUGINS, 1):
        plugin_id = plugin["id"]
        plugin_name = plugin["name"]
        repo = plugin["repo"]
        plugin_dir = os.path.join(PLUGINS_DIR, plugin_id)

        print(f"\n[{i}/{len(PLUGINS)}] {plugin_name} ({plugin_id})")
        print(f"  저장소: {repo}")

        os.makedirs(plugin_dir, exist_ok=True)

        downloaded_files = []
        for filename in FILES_TO_DOWNLOAD:
            url = get_latest_release_url(repo, filename)
            dest = os.path.join(plugin_dir, filename)
            print(f"  다운로드: {filename}...", end=" ")
            if download_file(url, dest):
                print("OK")
                downloaded_files.append(filename)
            else:
                if filename == "styles.css":
                    print("SKIP (선택사항)")
                else:
                    print("FAIL")

        if "main.js" in downloaded_files and "manifest.json" in downloaded_files:
            installed.append(plugin_id)
            print(f"  -> {plugin_name} 설치 성공!")
        else:
            failed.append(plugin_name)
            print(f"  -> {plugin_name} 설치 실패!")

    print("\n" + "=" * 50)
    print("  community-plugins.json 업데이트 중...")

    cp_path = os.path.join(PLUGINS_DIR, "community-plugins.json")
    existing = []
    if os.path.exists(cp_path):
        try:
            with open(cp_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            existing = []

    for pid in installed:
        if pid not in existing:
            existing.append(pid)

    with open(cp_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print("  -> community-plugins.json 업데이트 완료")

    print("\n" + "=" * 50)
    print("  설치 결과")
    print("=" * 50)
    print(f"\n  성공: {len(installed)}개")
    for pid in installed:
        print(f"    - {pid}")

    if failed:
        print(f"\n  실패: {len(failed)}개")
        for name in failed:
            print(f"    - {name}")

    print(f"\nObsidian을 재시작한 후 Settings > Community Plugins에서")
    print(f"각 플러그인을 활성화하세요.")


if __name__ == "__main__":
    main()
