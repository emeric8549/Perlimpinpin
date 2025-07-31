import tempfile, shutil, os, git, stat

def handle_remove_readonly(func, path):
    """Handle the removal of read-only files."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone_and_extract_code(github_url: str) -> str:
    tmp_dir = tempfile.mkdtemp()
    try:
        git.Repo.clone_from(github_url, tmp_dir, branch='main')
        code = ""
        for root, _, files in os.walk(tmp_dir):
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rb', '.php', '.html', '.css', '.json', '.xml', '.yaml', '.yml', '.md')):
                    try:
                        with open(os.path.join(root, file), 'r', errors='ignore') as f:
                            code += f.read() + "\n"
                    except Exception as e:
                        print(f"Error reading file {file}: {e}")
        return code[:100000]
    finally:
        shutil.rmtree(tmp_dir, onerror=handle_remove_readonly)