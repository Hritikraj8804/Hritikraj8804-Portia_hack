# 🤝 Contributing to DevOps AI Assistant

Thank you for your interest in contributing! This guide will help you get started.

## 🌟 Ways to Contribute

### 🐛 Bug Reports
- Report issues you encounter
- Provide detailed reproduction steps
- Include system information and logs

### 💡 Feature Requests
- Suggest new features or improvements
- Explain the use case and benefits
- Discuss implementation approaches

### 📝 Documentation
- Improve existing documentation
- Add examples and tutorials
- Fix typos and clarify instructions

### 💻 Code Contributions
- Fix bugs and implement features
- Improve performance and reliability
- Add tests and improve code quality

## 🚀 Getting Started

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/portia.git
cd portia
```

### 2. Set Up Development Environment
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

### 3. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Add your API keys (see API_KEYS.md for details)
# Edit .env with your keys
```

### 4. Test Your Setup
```bash
# Run tests to ensure everything works
python test_app.py

# Start the application
quick-start.bat  # Windows
# Or manually start both backend and frontend
```

## 🏗️ Development Workflow

### 1. Create a Branch
```bash
# Create feature branch from main
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

### 2. Make Changes
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed
- Test your changes thoroughly

### 3. Code Quality Checks
```bash
# Format code
black frontend/ backend/

# Check linting
flake8 frontend/ backend/

# Type checking (optional)
mypy frontend/ backend/
```

### 4. Test Your Changes
```bash
# Run existing tests
python test_app.py

# Test manually
# - Start the application
# - Test affected features
# - Verify no regressions
```

### 5. Commit and Push
```bash
# Add your changes
git add .

# Commit with descriptive message
git commit -m "feat: add pipeline filtering by date range"

# Push to your fork
git push origin feature/your-feature-name
```

### 6. Create Pull Request
1. Go to GitHub and create a pull request
2. Fill out the PR template
3. Link related issues
4. Wait for review and feedback

## 📋 Code Style Guidelines

### Python Code Style
- Follow **PEP 8** standards
- Use **Black** for code formatting
- Maximum line length: **88 characters**
- Use **type hints** where appropriate

### Example:
```python
def get_pipeline_status(repo_owner: str, repo_name: str) -> List[Dict[str, Any]]:
    """
    Get pipeline status for a specific repository.
    
    Args:
        repo_owner: GitHub repository owner
        repo_name: Repository name
        
    Returns:
        List of pipeline status dictionaries
    """
    # Implementation here
    pass
```

### Documentation Style
- Use **Markdown** for all documentation
- Include **code examples** where helpful
- Add **links** between related documents
- Keep language **clear and beginner-friendly**

### Commit Message Format
Use conventional commits format:
```
type(scope): description

feat(frontend): add pipeline filtering by status
fix(backend): resolve GitHub API rate limiting
docs(readme): update installation instructions
test(api): add tests for pipeline endpoints
```

**Types:**
- `feat` - New features
- `fix` - Bug fixes
- `docs` - Documentation changes
- `test` - Adding or updating tests
- `refactor` - Code refactoring
- `style` - Code style changes
- `chore` - Maintenance tasks

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
python test_app.py

# Test specific components
python -m pytest tests/  # If you add pytest tests
```

### Writing Tests
- Add tests for new features
- Test both success and error cases
- Mock external API calls
- Keep tests fast and reliable

### Test Structure
```python
def test_pipeline_status_parsing():
    """Test that pipeline status is parsed correctly."""
    # Arrange
    mock_response = {...}
    
    # Act
    result = parse_pipeline_status(mock_response)
    
    # Assert
    assert result['status'] == 'success'
    assert len(result['pipelines']) == 3
```

## 📁 Project Structure

```
portia/
├── backend/
│   └── simple_backend.py      # HTTP server and GitHub API
├── frontend/
│   └── app.py                 # Streamlit interface
├── docs/                      # Documentation files
├── tests/                     # Test files (if added)
├── .env.example              # Environment template
├── requirements.txt          # Dependencies
├── test_app.py              # Main test suite
└── README.md                # Project overview
```

### Key Files to Know
- **`backend/simple_backend.py`** - Main backend logic
- **`frontend/app.py`** - Streamlit UI and Portia integration
- **`test_app.py`** - Comprehensive test suite
- **`requirements.txt`** - Python dependencies

## 🔍 Areas for Contribution

### High Priority
- **Error handling improvements** - Better error messages and recovery
- **Performance optimization** - Faster data loading and caching
- **Test coverage** - More comprehensive testing
- **Documentation** - Examples and tutorials

### Medium Priority
- **UI/UX improvements** - Better design and user experience
- **Additional integrations** - Support for other CI/CD platforms
- **Advanced filtering** - More pipeline filtering options
- **Export features** - Data export and reporting

### Low Priority
- **Mobile responsiveness** - Better mobile interface
- **Themes and customization** - UI theming options
- **Advanced analytics** - Pipeline performance metrics
- **Notifications** - Alert system for failures

## 🐛 Bug Report Template

When reporting bugs, please include:

```markdown
**Bug Description**
A clear description of what the bug is.

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g., Windows 10]
- Python version: [e.g., 3.11.0]
- Browser: [e.g., Chrome 91]

**Additional Context**
- Error messages
- Screenshots
- Log files
```

## 💡 Feature Request Template

```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Use Case**
Explain why this feature would be useful.

**Proposed Solution**
Describe how you think this could be implemented.

**Alternatives Considered**
Other approaches you've thought about.

**Additional Context**
Any other relevant information.
```

## 📝 Pull Request Template

```markdown
**Description**
Brief description of changes made.

**Type of Change**
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

**Testing**
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

**Checklist**
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## 🤝 Code Review Process

### For Contributors
- Be open to feedback and suggestions
- Respond to review comments promptly
- Make requested changes in separate commits
- Ask questions if feedback is unclear

### For Reviewers
- Be constructive and helpful
- Focus on code quality and maintainability
- Suggest improvements, don't just point out problems
- Approve when ready, request changes when needed

## 🏆 Recognition

Contributors will be recognized in:
- **README.md** - Contributors section
- **Release notes** - Feature acknowledgments
- **GitHub** - Contributor graphs and statistics

## 📞 Getting Help

### Development Questions
- Open a **GitHub Discussion**
- Ask in **pull request comments**
- Create an **issue** for guidance

### Community Guidelines
- Be respectful and inclusive
- Help others learn and grow
- Share knowledge and experiences
- Follow the code of conduct

## 📚 Resources

### Learning Resources
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Portia AI Documentation](https://docs.portialabs.ai/)

### Development Tools
- **VS Code** - Recommended editor with Python extension
- **Git** - Version control
- **Postman** - API testing
- **GitHub Desktop** - GUI for Git operations

---

**Ready to contribute?** 🚀 Start by forking the repository and following the setup guide above!

**Questions?** Open an issue or discussion on GitHub - we're here to help!