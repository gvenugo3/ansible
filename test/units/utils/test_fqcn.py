# coding: utf-8
# (c) 2020, Felix Fontein <felix@fontein.de>
# (c) 2025, Ansible Project
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

import pytest

from ansible.utils.fqcn import add_internal_fqcns


class TestAddInternalFqcns:
    """Test the add_internal_fqcns function."""

    def test_empty_list(self):
        """Test with empty input list."""
        result = add_internal_fqcns([])
        assert result == []

    def test_single_simple_name(self):
        """Test with single simple module name."""
        result = add_internal_fqcns(['copy'])
        expected = ['copy', 'ansible.builtin.copy', 'ansible.legacy.copy']
        assert result == expected

    def test_single_fqcn(self):
        """Test with single fully qualified collection name."""
        result = add_internal_fqcns(['community.general.git'])
        expected = ['community.general.git']
        assert result == expected

    def test_mixed_names(self):
        """Test with mix of simple names and FQCNs."""
        input_names = ['copy', 'community.general.git', 'file']
        result = add_internal_fqcns(input_names)
        expected = [
            'copy',
            'ansible.builtin.copy',
            'ansible.legacy.copy',
            'community.general.git',
            'file',
            'ansible.builtin.file',
            'ansible.legacy.file'
        ]
        assert result == expected

    def test_multiple_simple_names(self):
        """Test with multiple simple module names."""
        input_names = ['copy', 'file', 'template']
        result = add_internal_fqcns(input_names)
        expected = [
            'copy',
            'ansible.builtin.copy',
            'ansible.legacy.copy',
            'file',
            'ansible.builtin.file',
            'ansible.legacy.file',
            'template',
            'ansible.builtin.template',
            'ansible.legacy.template'
        ]
        assert result == expected

    def test_multiple_fqcns(self):
        """Test with multiple FQCNs."""
        input_names = ['community.general.git', 'ansible.posix.mount', 'community.crypto.openssl_certificate']
        result = add_internal_fqcns(input_names)
        expected = ['community.general.git', 'ansible.posix.mount', 'community.crypto.openssl_certificate']
        assert result == expected

    def test_builtin_fqcn(self):
        """Test with ansible.builtin FQCN."""
        result = add_internal_fqcns(['ansible.builtin.copy'])
        expected = ['ansible.builtin.copy']
        assert result == expected

    def test_legacy_fqcn(self):
        """Test with ansible.legacy FQCN."""
        result = add_internal_fqcns(['ansible.legacy.copy'])
        expected = ['ansible.legacy.copy']
        assert result == expected

    def test_preserve_order(self):
        """Test that the original order is preserved."""
        input_names = ['file', 'copy', 'template']
        result = add_internal_fqcns(input_names)
        expected = [
            'file',
            'ansible.builtin.file',
            'ansible.legacy.file',
            'copy',
            'ansible.builtin.copy',
            'ansible.legacy.copy',
            'template',
            'ansible.builtin.template',
            'ansible.legacy.template'
        ]
        assert result == expected

    def test_single_character_name(self):
        """Test with single character module name."""
        result = add_internal_fqcns(['a'])
        expected = ['a', 'ansible.builtin.a', 'ansible.legacy.a']
        assert result == expected

    def test_numeric_name(self):
        """Test with numeric module name."""
        result = add_internal_fqcns(['123'])
        expected = ['123', 'ansible.builtin.123', 'ansible.legacy.123']
        assert result == expected

    def test_underscore_name(self):
        """Test with underscore in module name."""
        result = add_internal_fqcns(['my_module'])
        expected = ['my_module', 'ansible.builtin.my_module', 'ansible.legacy.my_module']
        assert result == expected

    def test_hyphen_name(self):
        """Test with hyphen in module name."""
        result = add_internal_fqcns(['my-module'])
        expected = ['my-module', 'ansible.builtin.my-module', 'ansible.legacy.my-module']
        assert result == expected

    def test_empty_string_name(self):
        """Test with empty string as module name."""
        result = add_internal_fqcns([''])
        expected = ['', 'ansible.builtin.', 'ansible.legacy.']
        assert result == expected

    def test_dot_in_simple_name(self):
        """Test behavior with dots in what looks like simple names."""
        # Names with dots should be treated as FQCNs
        result = add_internal_fqcns(['a.b'])
        expected = ['a.b']
        assert result == expected

    def test_multiple_dots(self):
        """Test with multiple dots in name."""
        result = add_internal_fqcns(['a.b.c.d'])
        expected = ['a.b.c.d']
        assert result == expected

    def test_name_starting_with_dot(self):
        """Test with name starting with dot."""
        result = add_internal_fqcns(['.module'])
        expected = ['.module']
        assert result == expected

    def test_name_ending_with_dot(self):
        """Test with name ending with dot."""
        result = add_internal_fqcns(['module.'])
        expected = ['module.']
        assert result == expected

    def test_duplicate_names(self):
        """Test with duplicate names in input."""
        input_names = ['copy', 'copy', 'file']
        result = add_internal_fqcns(input_names)
        expected = [
            'copy',
            'ansible.builtin.copy',
            'ansible.legacy.copy',
            'copy',
            'ansible.builtin.copy',
            'ansible.legacy.copy',
            'file',
            'ansible.builtin.file',
            'ansible.legacy.file'
        ]
        assert result == expected

    def test_special_characters(self):
        """Test with special characters in module names."""
        input_names = ['module@name', 'module#name', 'module!name']
        result = add_internal_fqcns(input_names)
        expected = [
            'module@name',
            'ansible.builtin.module@name',
            'ansible.legacy.module@name',
            'module#name',
            'ansible.builtin.module#name',
            'ansible.legacy.module#name',
            'module!name',
            'ansible.builtin.module!name',
            'ansible.legacy.module!name'
        ]
        assert result == expected

    def test_long_fqcn(self):
        """Test with very long FQCN."""
        long_fqcn = 'very.long.collection.name.with.many.parts.module_name'
        result = add_internal_fqcns([long_fqcn])
        expected = [long_fqcn]
        assert result == expected

    def test_return_type(self):
        """Test that return type is list."""
        result = add_internal_fqcns(['copy'])
        assert isinstance(result, list)
        assert all(isinstance(item, str) for item in result)

    def test_input_not_modified(self):
        """Test that input list is not modified."""
        input_names = ['copy', 'file']
        original_input = input_names.copy()
        add_internal_fqcns(input_names)
        assert input_names == original_input

    def test_non_string_input(self):
        """Test behavior with non-string input (should fail gracefully)."""
        # The function expects strings, non-strings should raise TypeError
        with pytest.raises(TypeError):
            add_internal_fqcns([123])

    @pytest.mark.parametrize("input_names, expected", [
        # Edge cases
        ([''], ['', 'ansible.builtin.', 'ansible.legacy.']),
        (['a'], ['a', 'ansible.builtin.a', 'ansible.legacy.a']),
        (['a.b'], ['a.b']),
        (['a.b.c'], ['a.b.c']),

        # Real-world examples
        (['ping'], ['ping', 'ansible.builtin.ping', 'ansible.legacy.ping']),
        (['debug'], ['debug', 'ansible.builtin.debug', 'ansible.legacy.debug']),
        (['community.general.git'], ['community.general.git']),
        (['ansible.posix.mount'], ['ansible.posix.mount']),

        # Mixed scenarios
        (['ping', 'community.general.git'],
         ['ping', 'ansible.builtin.ping', 'ansible.legacy.ping', 'community.general.git']),
        (['ansible.builtin.copy', 'file'],
         ['ansible.builtin.copy', 'file', 'ansible.builtin.file', 'ansible.legacy.file']),
    ])
    def test_parametrized_scenarios(self, input_names, expected):
        """Test various scenarios with parametrized inputs."""
        result = add_internal_fqcns(input_names)
        assert result == expected


class TestAddInternalFqcnsIntegration:
    """Integration tests for add_internal_fqcns function."""

    def test_common_ansible_modules(self):
        """Test with common Ansible module names."""
        common_modules = [
            'copy', 'file', 'template', 'lineinfile', 'service', 'yum', 'apt',
            'user', 'group', 'command', 'shell', 'script', 'ping', 'debug'
        ]
        result = add_internal_fqcns(common_modules)

        # Should have original names plus builtin and legacy variants
        assert len(result) == len(common_modules) * 3

        # Check that all original names are present
        for module in common_modules:
            assert module in result
            assert f'ansible.builtin.{module}' in result
            assert f'ansible.legacy.{module}' in result

    def test_mixed_module_types(self):
        """Test with a realistic mix of module types."""
        mixed_modules = [
            'copy',                          # Simple name
            'community.general.git',         # Community collection
            'ansible.posix.mount',           # Ansible collection
            'template',                      # Another simple name
            'community.crypto.openssl_certificate',  # Long collection name
            'ansible.builtin.debug',         # Already builtin
            'file'                           # Another simple name
        ]

        result = add_internal_fqcns(mixed_modules)

        # Check specific expected behavior
        assert 'copy' in result
        assert 'ansible.builtin.copy' in result
        assert 'ansible.legacy.copy' in result

        # FQCNs should not be expanded
        assert 'community.general.git' in result
        assert 'ansible.builtin.community.general.git' not in result

        # Already builtin should not be expanded
        assert 'ansible.builtin.debug' in result
        assert 'ansible.builtin.ansible.builtin.debug' not in result

    def test_action_plugin_scenario(self):
        """Test scenario similar to action plugin resolution."""
        # This simulates how the function might be used in action plugin resolution
        actions = ['setup', 'gather_facts', 'include_tasks', 'import_tasks']
        result = add_internal_fqcns(actions)

        # Each action should have builtin and legacy variants
        for action in actions:
            assert action in result
            assert f'ansible.builtin.{action}' in result
            assert f'ansible.legacy.{action}' in result

    def test_performance_large_list(self):
        """Test performance with a large number of module names."""
        # Generate a large list of module names
        large_list = [f'module_{i}' for i in range(1000)]

        result = add_internal_fqcns(large_list)

        # Should have 3x the original size
        assert len(result) == 3000

        # Check first and last entries
        assert 'module_0' in result
        assert 'ansible.builtin.module_0' in result
        assert 'ansible.legacy.module_0' in result
        assert 'module_999' in result
        assert 'ansible.builtin.module_999' in result
        assert 'ansible.legacy.module_999' in result

    def test_generator_input(self):
        """Test with generator input."""
        # Test that the function works with iterables other than lists
        generator = (name for name in ['copy', 'file', 'template'])
        result = add_internal_fqcns(generator)

        expected = [
            'copy', 'ansible.builtin.copy', 'ansible.legacy.copy',
            'file', 'ansible.builtin.file', 'ansible.legacy.file',
            'template', 'ansible.builtin.template', 'ansible.legacy.template'
        ]
        assert result == expected

    def test_tuple_input(self):
        """Test with tuple input."""
        input_tuple = ('copy', 'file', 'template')
        result = add_internal_fqcns(input_tuple)

        expected = [
            'copy', 'ansible.builtin.copy', 'ansible.legacy.copy',
            'file', 'ansible.builtin.file', 'ansible.legacy.file',
            'template', 'ansible.builtin.template', 'ansible.legacy.template'
        ]
        assert result == expected
