# Maintainer Notes for Primary Account

## Overview

Guidelines and reminders for maintaining the CardioRetina-AI repository.

## Repository Maintenance

### Regular Tasks

#### Weekly
- [ ] Review open issues
- [ ] Respond to pull requests
- [ ] Check for security advisories in dependencies
- [ ] Monitor CI/CD pipeline status

#### Monthly
- [ ] Update dependencies (carefully)
- [ ] Review and merge documentation improvements
- [ ] Check for broken links in documentation
- [ ] Review analytics (if enabled)

#### Quarterly
- [ ] Archive stale issues
- [ ] Update screenshots if UI changed
- [ ] Review and update README
- [ ] Assess project roadmap progress

### Issue Management

#### Labeling System

| Label | Use For | Color |
|-------|---------|-------|
| `bug` | Something broken | Red |
| `enhancement` | New feature request | Green |
| `documentation` | Docs improvements | Blue |
| `question` | User questions | Purple |
| `good first issue` | Easy for newcomers | Light green |
| `help wanted` | Maintainer needs assistance | Orange |
| `wontfix` | Out of scope | Gray |
| `duplicate` | Already reported | Gray |

#### Triage Process

1. **New issues**: Label within 24 hours
2. **Questions**: Answer or convert to discussion
3. **Bugs**: Reproduce before labeling confirmed
4. **Feature requests**: Assess alignment with project scope
5. **PRs**: Review within 1 week

### Pull Request Guidelines

#### Accepting PRs

✅ **Auto-merge**:
- Documentation fixes (typos, clarifications)
- Additional tests (no core logic change)
- Dependency updates (patch versions)

⚠️ **Manual review required**:
- Code changes
- Architecture modifications
- New dependencies
- Breaking changes

❌ **Don't merge**:
- Untested code
- No description provided
- Conflicts with main
- CI/CD failing

#### Review Checklist

- [ ] Code follows existing style
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or properly documented)
- [ ] Commit messages are clear
- [ ] CLA signed (if required)

## Communication Guidelines

### With Users

#### Tone
- Professional but friendly
- Encouraging to newcomers
- Clear about limitations
- Patient with questions

#### Key Messages to Reinforce

1. **Research prototype only**
   - "This is a research prototype, not for clinical use"
   - "Always consult healthcare professionals"
   - "Not FDA approved or clinically validated"

2. **Educational purpose**
   - "Designed for learning medical AI"
   - "Demonstrates best practices"
   - "Open for research and education"

3. **Contribution welcome**
   - "Issues and PRs welcome"
   - "Documentation improvements appreciated"
   - "Community-driven project"

### Handling Common Questions

| Question | Response Template |
|----------|-----------------|
| "Can I use this in my hospital?" | "No, this is a research prototype not intended for clinical use. Clinical deployment would require extensive validation and regulatory approval." |
| "What's the accuracy?" | "Accuracy depends on the dataset used. The project includes evaluation tools to measure performance on your data. See MODEL_CARD.md for methodology." |
| "Can you add [feature]?" | "Thanks for the suggestion! Please open an issue to discuss. Community contributions are welcome." |
| "I found a bug" | "Thanks for reporting! Please include steps to reproduce, expected vs actual behavior, and your environment details." |

## Security Considerations

### Dependency Management

```bash
# Check for vulnerabilities
pip audit

# Update carefully
pip list --outdated

# Test after updates
pytest tests/ -v
```

### Sensitive Data

⚠️ **Watch for**:
- Accidental commit of real patient data
- API keys in commits
- Personal information in issues

**If found**:
1. Remove immediately
2. Force push if needed
3. Document incident
4. Notify if data breach occurred

## Release Process

### Version Numbering (Semantic Versioning)

```
MAJOR.MINOR.PATCH
1.0.0
```

- **MAJOR**: Breaking changes
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes

### Release Checklist

1. **Preparation**
   - [ ] Update version in `pyproject.toml`
   - [ ] Update CHANGELOG.md
   - [ ] Update README if needed
   - [ ] Run full test suite
   - [ ] Update MODEL_CARD.md if model changed

2. **Tagging**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

3. **Release Notes**
   - Create GitHub release
   - Copy CHANGELOG section
   - Attach binaries if applicable

4. **Post-Release**
   - [ ] Announce (if appropriate)
   - [ ] Update documentation site
   - [ ] Monitor for issues

## Documentation Maintenance

### README Updates

Update when:
- New features added
- Installation process changes
- API changes
- Major bug fixes

### Model Card Updates

Update when:
- Architecture changes
- New evaluation results
- Different dataset used
- Limitations discovered

### docs/ Folder

Organization:
```
docs/
├── 01-*.md    # Overview docs
├── 10-*.md    # Technical guides
├── 20-*.md    # Ethics and safety
├── 30-*.md    # Presentation materials
└── README.md  # Docs index
```

## Community Building

### Encouraging Contributions

- Label `good first issue` for newcomers
- Respond promptly to first-time contributors
- Thank contributors in release notes
- Feature significant contributions

### Setting Boundaries

**Not in scope**:
- Clinical validation (requires institutional partnership)
- Regulatory approval (requires significant resources)
- Real patient data (privacy concerns)
- Commercial support

**Redirect to**:
- Research institutions for clinical validation
- Commercial vendors for production systems
- Consulting services for custom development

## Legal and Ethical Reminders

### License Compliance

- MIT License allows broad use
- Must include license in distributions
- Third-party dependencies have their own licenses

### Ethical Obligations

- Never claim clinical validation
- Always include disclaimers
- Be honest about limitations
- Protect user privacy
- Avoid enabling misuse

### Documentation to Maintain

Must always be accurate:
- README disclaimer
- MODEL_CARD intended use
- All "not for clinical use" statements
- Limitations sections

## Personal Notes

### Time Management

- **Quick wins**: Documentation fixes, typos (5-10 min)
- **Medium tasks**: Issue responses, small PRs (30-60 min)
- **Deep work**: Major features, architecture changes (hours)

### Sustainability

- Don't burn out
- It's okay to delay responses
- Set boundaries on scope
- Community can help

### Learning Opportunities

- Each issue is a teaching moment
- Document solutions for future reference
- Share knowledge in discussions
- Admit when you don't know

---

*Maintaining an open source project is a marathon, not a sprint. Prioritize sustainability and community health.*
