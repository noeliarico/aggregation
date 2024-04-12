# Table of contents

- [Table of contents](#table-of-contents)
- [Package installation](#package-installation)
- [Create package distributable](#create-package-distributable)
- [Commits guide](#commits-guide)

# Package installation

```
pip install aggregation
```

# Create package distributable

Run `py -m pip install --upgrade build` and then, on the root folder of the project, run `py -m build`. This will generate the distributable, which can be installed locally by executing `pip install .\dist\ranking_aggregation-<version>.tar.gz`.

References:

- [Packaging and distributing projects - Python Packaging User Guide](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/)

- [Packaging Python Projects - Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

# Commits guide

```
♻️ [Change functionality] ♻️
⚡️ [Improve code] ⚡️
🐛 [Fix bug] 🐛
🩹 [Fix non critical bug] 🩹
🚑️ [Critical Hotfix] 🚑️
✅ [Add feature] ✅
✨ [Add small feature] ✨
🩺 [Add sanity check] 🩺
🧪 [Add non tested feature]
🎉 [Feature passed a test]
🚧 [Feature not completed] 🚧
💥 [Add breaking changes] 💥
➕ [Add dependency] ➕
➖ [Remove dependency] ➖
🗑️ [Remove] 🗑️
📝 [Document] 📝
🔀 [Merge] 🔀
🎨 [Code formatting] 🎨
🔒️ [Fix security issues] 🔒️
🚀 [Built deployment package] 🚀
```
