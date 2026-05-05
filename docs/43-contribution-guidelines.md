# Contribution Guidelines for Research Prototype

## Overview

Guidelines for contributing to CardioRetina-AI while maintaining its research prototype nature.

## Ways to Contribute

### 1. Documentation (Easiest)

**What we need**:
- Typo fixes and clarifications
- Additional examples
- Tutorial notebooks
- Translation to other languages
- Improved explanations

**How to contribute**:
1. Find an issue with `documentation` label OR identify improvement
2. Edit the relevant `.md` file
3. Submit PR with clear description

**Example contributions**:
- Fix grammar in README
- Add more troubleshooting examples
- Create Jupyter notebook demo
- Translate key documents

### 2. Bug Fixes

**What we need**:
- Fix reported bugs
- Resolve deprecation warnings
- Improve error messages
- Fix edge cases

**How to contribute**:
1. Check existing issues with `bug` label
2. Comment that you're working on it
3. Write fix with test
4. Submit PR referencing issue

**Requirements**:
- Include test case that fails before, passes after
- Update documentation if behavior changes
- Follow existing code style

### 3. Tests

**What we need**:
- Increase test coverage
- Add integration tests
- Property-based tests
- Performance benchmarks

**How to contribute**:
1. Check current coverage: `pytest --cov=cardioretina`
2. Identify untested code
3. Write tests
4. Submit PR

**Requirements**:
- Tests should be deterministic
- Use fixtures for common setup
- Mock external dependencies
- Document test purpose

### 4. Code Improvements

**What we accept**:
- Refactoring for clarity
- Performance optimizations
- Better error handling
- Type hints additions

**What requires discussion first**:
- New features
- Architecture changes
- New dependencies
- API modifications

## Contribution Process

### Step 1: Before Starting

1. **Check existing issues**: Your idea might already be discussed
2. **Open an issue** (for non-trivial changes): Describe what you want to do
3. **Wait for feedback**: Maintainers will provide guidance
4. **Get approval**: For significant changes, wait for green light

### Step 2: Development

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/cardioretina-ai.git

# 2. Create branch
git checkout -b feature/your-feature-name

# 3. Make changes
# Edit files...

# 4. Test
pytest tests/ -v
ruff check cardioretina/ tests/

# 5. Commit
git add .
git commit -m "feat: add new feature"

# 6. Push
git push origin feature/your-feature-name
```

### Step 3: Pull Request

**PR Title Format**:
```
type: brief description

Examples:
docs: fix typo in README
feat: add batch inference endpoint
fix: handle missing clinical data
```

**PR Description Template**:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactoring
- [ ] Tests

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

## Related Issues
Fixes #123
```

## Code Standards

### Python Style

Follow PEP 8 with these specifics:

```python
# Line length: 100 characters
# Use type hints
def process_image(image: Image.Image) -> torch.Tensor:
    """Process image for model input.
    
    Args:
        image: PIL Image object
        
    Returns:
        Preprocessed tensor
    """
    ...

# Docstrings for public functions
# Comments for complex logic
# Clear variable names
```

### Testing

```python
def test_feature():
    """Test description."""
    # Arrange
    input_data = ...
    expected = ...
    
    # Act
    result = function(input_data)
    
    # Assert
    assert result == expected
```

### Documentation

```markdown
# Header

Description of feature.

## Subsection

- Bullet points
- For clarity

```python
# Code examples
```

> Important notes
```

## Scope Boundaries

### ✅ In Scope (Welcome)

- Documentation improvements
- Bug fixes
- Test additions
- Code refactoring
- Performance optimizations
- Example notebooks
- UI/UX improvements (web dashboard)

### ⚠️ Discuss First

- New model architectures
- New API endpoints
- New dependencies
- Breaking changes
- Major refactoring

### ❌ Out of Scope (Will Not Accept)

- Real patient data
- Clinical validation results
- Proprietary algorithms
- Commercial features
- Removal of research disclaimers
- Claims of clinical readiness

## Research Prototype Considerations

### Important Reminders

1. **Maintain disclaimers**: All contributions must preserve "research prototype" messaging
2. **No clinical claims**: Don't add statements implying clinical validation
3. **Ethical considerations**: Changes affecting fairness or bias need careful review
4. **Documentation focus**: Prioritize documentation over new features

### Acceptable Changes

✅ **Documentation**:
- Clarify limitations
- Add ethical considerations
- Improve installation guide
- Add more examples

✅ **Code**:
- Fix bugs
- Add tests
- Improve performance
- Refactor for clarity

✅ **Research**:
- Ablation studies
- Evaluation metrics
- Comparison experiments
- Methodology documentation

### Unacceptable Changes

❌ **Clinical claims**:
- "FDA approved"
- "Clinically validated"
- "For diagnostic use"
- Removal of disclaimers

❌ **Harmful modifications**:
- Removing bias checks
- Disabling explainability
- Bypassing safety checks

## Review Process

### What Reviewers Look For

1. **Code quality**: Readable, maintainable, tested
2. **Documentation**: Clear, accurate, complete
3. **Scope alignment**: Fits project goals
4. **Safety**: No harmful changes
5. **Ethics**: Considers fairness and bias

### Review Timeline

- **Simple changes** (docs, typos): 1-3 days
- **Medium changes** (bug fixes, tests): 3-7 days
- **Complex changes** (features, architecture): 1-2 weeks

### After Approval

- Squash commits if requested
- Update branch if needed
- Maintainer will merge

## Recognition

### Contributors

All contributors will be:
- Listed in CONTRIBUTORS.md (if created)
- Thanked in release notes
- Credited in relevant documentation

### Significant Contributions

For substantial contributions:
- Co-authorship consideration for publications
- Feature highlight in README
- Special thanks in presentations

## Questions?

### Before Contributing

- Read this guide completely
- Check existing issues
- Review similar merged PRs

### Getting Help

- Open a discussion for questions
- Comment on relevant issue
- Tag maintainers if stuck

### Feedback

- This is a learning project
- Constructive feedback welcome
- Beginners encouraged
- Mentorship available

---

*Contributions make open source projects vibrant and useful. Thank you for considering contributing to CardioRetina-AI!*
