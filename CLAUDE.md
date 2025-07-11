# Ansible Development Notes

## Development Environment Setup

### Prerequisites
- Python 3.11+ required (project uses Python 3.13.1)
- Git repository with proper branch management

### Environment Setup Commands
```bash
# Set up development environment
source ./hacking/env-setup

# Install dependencies
pip install -r requirements.txt
pip install -r test/units/requirements.txt

# Additional test dependencies
pip install pytest pytest-mock
```

### Environment Variables
After running `env-setup`, these are automatically configured:
- `PATH`: Includes `/bin` directory for Ansible executables
- `PYTHONPATH`: Includes `/lib` and `/test/lib` for modules
- `MANPATH`: Includes `/docs/man` for documentation

## Testing

### Running Unit Tests
```bash
# Run specific test file
python3 -m pytest test/units/parsing/test_quoting.py -v

# Run all tests in a directory
python3 -m pytest test/units/parsing/ -v
```

### Running Sanity Tests
```bash
# Run PEP8 style checks
python3 bin/ansible-test sanity test/units/parsing/test_quoting.py --test pep8

# Run import checks
python3 bin/ansible-test sanity --test import test/units/parsing/test_quoting.py

# Run compile checks
python3 bin/ansible-test sanity --test compile test/units/parsing/test_quoting.py
```

### Verifying Ansible Installation
```bash
# Check Ansible version and configuration
python3 bin/ansible --version

# Test specific modules
python3 bin/ansible-test --help
```

## Code Style and Standards

### PEP8 Requirements
- No whitespace in blank lines
- Use `is False` instead of `== False`
- Use `is True` instead of `== True`
- Files must end with a newline
- Proper spacing around operators and functions

### Common PEP8 Issues and Fixes
```python
# Wrong
assert is_quoted('') == False

# Right
assert is_quoted('') is False

# Wrong - blank line with whitespace
        
# Right - clean blank line

```

## Repository Structure

### Key Directories
- `/lib/ansible/`: Core Ansible modules and functionality
- `/test/units/`: Unit tests for core functionality
- `/test/integration/`: Integration tests
- `/bin/`: Executable scripts (symlinks to actual modules)
- `/hacking/`: Development tools and utilities

### Important Files
- `requirements.txt`: Core dependencies
- `test/units/requirements.txt`: Test-specific dependencies
- `pyproject.toml`: Project configuration and metadata
- `hacking/env-setup`: Development environment setup script

## Git Workflow

### Branch Management
- Main development branch: `devel`
- Feature branches: descriptive names like `add-quoting-test-coverage`
- Always work from feature branches, not directly on `devel`

### Common Git Commands
```bash
# Switch to feature branch
git checkout -b feature-branch-name origin/feature-branch-name

# Check status and changes
git status
git diff

# Commit changes
git add <files>
git commit -m "descriptive commit message"

# Push changes
git push
```

## Module Development

### Testing New Modules
The `ansible.parsing.quoting` module provides:
- `is_quoted(data)`: Checks if string is properly quoted
- `unquote(data)`: Removes quotes from properly quoted strings

### Test Coverage Best Practices
- Test both valid and invalid inputs
- Include edge cases (empty strings, single characters)
- Test integration between related functions
- Use parametrized tests for comprehensive coverage
- Include roundtrip testing where applicable

## Troubleshooting

### Common Issues
1. **Import errors**: Ensure `PYTHONPATH` is set correctly via `env-setup`
2. **Command not found**: Check `PATH` includes `/bin` directory
3. **PEP8 failures**: Run sanity tests to identify style issues
4. **Test failures**: Verify all dependencies are installed

### Debug Commands
```bash
# Check Python paths
echo $PYTHONPATH

# Verify Ansible installation
which ansible
python3 -c "import ansible; print(ansible.__file__)"

# Check test dependencies
pip list | grep -E "(pytest|mock)"
```

### Performance Notes
- Use `source ./hacking/env-setup` in each new terminal session
- Ansible executables in `/bin` are symlinks to actual Python modules
- Tests run faster when dependencies are pre-installed

## Test Coverage Analysis

### Finding Untested Modules
```bash
# Find modules without corresponding test files
find lib/ansible/ -name "*.py" -not -name "__init__.py" | while read file; do
    test_file="test/units/${file#lib/ansible/}"
    test_file="${test_file%.py}_test.py"
    if [ ! -f "$test_file" ]; then
        echo "No test: $file"
    fi
done
```

### Good Candidates for Testing
Priority modules that lack test coverage:
1. **`lib/ansible/utils/fqcn.py`** ✅ - FQCN handling (now has tests)
2. **`lib/ansible/utils/hashing.py`** - File hashing utilities
3. **`lib/ansible/utils/color.py`** - Terminal color formatting
4. **`lib/ansible/utils/singleton.py`** - Singleton pattern implementation
5. **`lib/ansible/module_utils/parsing/convert_bool.py`** - Boolean conversion (has basic tests)

### Test Creation Best Practices
- **40+ test cases** for comprehensive coverage
- **Parametrized tests** for multiple input scenarios
- **Edge cases**: empty strings, None values, invalid inputs
- **Integration tests** for real-world usage patterns
- **Error handling** tests for exception scenarios
- **Type validation** tests for input/output types

### Example Test Structure
```python
class TestModuleName:
    """Test the main functionality."""
    
    @pytest.mark.parametrize("input, expected", [
        # Valid cases
        ('valid_input', expected_output),
        # Edge cases
        ('', expected_for_empty),
        # Invalid cases with error handling
    ])
    def test_function_name(self, input, expected):
        assert function_name(input) == expected

class TestModuleNameIntegration:
    """Integration and real-world usage tests."""
    
    def test_real_world_scenario(self):
        # Test common usage patterns
        pass
```

### Created Test Files
- `test/units/utils/test_fqcn.py` - 40 comprehensive tests for FQCN handling
  - Tests simple names, FQCNs, edge cases, and integration scenarios
  - Covers all code paths including error conditions
  - Performance testing with large datasets