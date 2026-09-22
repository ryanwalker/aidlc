import asyncio

from claude_agent_sdk import PermissionResultAllow, PermissionResultDeny, ToolPermissionContext

from agent_harness.permissions import enforce_directory_restrictions


def _ctx(agent_id: str | None) -> ToolPermissionContext:
    return ToolPermissionContext(agent_id=agent_id)


def _check(tool_name: str, tool_input: dict, agent_id: str | None):
    return asyncio.run(enforce_directory_restrictions(tool_name, tool_input, _ctx(agent_id)))


def test_implementer_blocked_from_reading_tests_dir():
    result = _check("Read", {"file_path": "tests/test_foo.py"}, "implementer")
    assert isinstance(result, PermissionResultDeny)


def test_implementer_blocked_from_writing_nested_tests_path():
    result = _check(
        "Write", {"file_path": "src/agent_harness/tests/helpers.py"}, "implementer"
    )
    assert isinstance(result, PermissionResultDeny)


def test_implementer_blocked_from_bash_referencing_tests_dir():
    result = _check("Bash", {"command": "cat tests/test_foo.py"}, "implementer")
    assert isinstance(result, PermissionResultDeny)


def test_implementer_allowed_to_edit_src():
    result = _check("Edit", {"file_path": "src/agent_harness/runner.py"}, "implementer")
    assert isinstance(result, PermissionResultAllow)


def test_other_agents_unaffected():
    result = _check("Read", {"file_path": "tests/test_foo.py"}, "test-writer")
    assert isinstance(result, PermissionResultAllow)


def test_main_agent_no_id_unaffected():
    result = _check("Read", {"file_path": "tests/test_foo.py"}, None)
    assert isinstance(result, PermissionResultAllow)
