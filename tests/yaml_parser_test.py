import pytest
import yaml

from yaml_parser import PypyarusYamlParser, PapyrusSchema

# -----------------------------------------------------------------------------
# __load_yaml
# -----------------------------------------------------------------------------
def test_load_yaml():
    """Test loading a valid YAML file."""
    yaml_file = 'tests/yaml_test_files/pypyrus.test.yaml'

    parser = PypyarusYamlParser(yaml_file)

    assert len(parser.get_data()) > 0


@pytest.mark.parametrize("yaml_file, expected_exception", [
    ('tests/pypyrus_invalid.test.yaml', FileNotFoundError),
    ('tests/yaml_test_files/pypyrus.invalid.yaml', yaml.scanner.ScannerError),
])
def test_load_yaml_fail(yaml_file, expected_exception):
    """Test handling of fails."""
    with pytest.raises(expected_exception):
        parser = PypyarusYamlParser(yaml_file)

# -----------------------------------------------------------------------------
# validate
# -----------------------------------------------------------------------------
def test_validate_with_valid_data():
    """Test validation with valid data."""
    # Arrange
    yaml_file = 'tests/yaml_test_files/pypyrus.test.yaml'
    parser = PypyarusYamlParser(yaml_file)
    
    # Act
    schema = parser.validate()

    # Assert
    assert schema is not None
    assert type(schema) == PapyrusSchema

def test_validate_with_invalid_data():
    """Test validation with invalid data."""
    # Arrange
    yaml_file = 'tests/yaml_test_files/pypyrus.wrong_schema.yaml'
    
    # Act
    with pytest.raises(ValueError):
        parser = PypyarusYamlParser(yaml_file)
        parser.validate()