# 在解壓後的 69 資料夾執行；變數只影響這個子 shell。
(
  export GEMINI_CLI_HOME="$(pwd)/memory-lab/isolated-user"
  cd memory-lab/project || exit 1
  git init
  gemini --version
  gemini
)
