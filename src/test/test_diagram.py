from umleditor.mvc_model import Diagram
"""
These test that the basic functions for Diagram interact
with the other classes. The individual classes/functions
are tested more thoroughly in other test files.
"""
def test_create_diagram():
    dia = Diagram()
    assert dia

def test_dia_add_entity():
    dia = Diagram()
    assert not dia.has_entity("ent")
    dia.add_entity("ent")
    assert dia.has_entity("ent")

def test_dia_add_multiple_entities():
    dia = Diagram()
    assert not dia.has_entity("ent1")
    assert not dia.has_entity("ent2")
    assert not dia.has_entity("ent3")
    dia.add_entity("ent1")
    dia.add_entity("ent2")
    assert dia.has_entity("ent1")
    assert dia.has_entity("ent2")
    assert not dia.has_entity("ent3")
    dia.add_entity("ent3")
    assert dia.has_entity("ent1")
    assert dia.has_entity("ent2")
    assert dia.has_entity("ent3")

def test_dia_get_entity():
    dia = Diagram()
    assert not dia.has_entity("ent4")
    dia.add_entity("ent4")
    ent5 = dia.get_entity("ent4")
    assert ent5
    assert ent5.get_name() == "ent4"
    assert ent5.get_name() != "ent5"
    assert dia.has_entity("ent4")

def test_dia_delete_entity():
    dia = Diagram()
    assert not dia.has_entity("ent6")
    dia.add_entity("ent6")
    assert dia.has_entity("ent6")
    dia.delete_entity("ent6")
    assert not dia.has_entity("ent6")

def test_dia_delete_multiple_entities():
    dia = Diagram()
    dia.add_entity("ent7")
    dia.add_entity("ent8")
    dia.add_entity("ent9")
    assert dia.has_entity("ent7")
    assert dia.has_entity("ent8")
    assert dia.has_entity("ent9")
    dia.delete_entity("ent7")
    dia.delete_entity("ent8")
    assert not dia.has_entity("ent7")
    assert not dia.has_entity("ent8")
    assert dia.has_entity("ent9")
    dia.delete_entity("ent9")
    assert not dia.has_entity("ent7")
    assert not dia.has_entity("ent8")
    assert not dia.has_entity("ent9")

def test_dia_rename_entity():
    dia = Diagram()
    dia.add_entity("ent10")
    assert dia.has_entity("ent10")
    assert not dia.has_entity("ent11")
    dia.rename_entity("ent10", "ent11")
    assert not dia.has_entity("ent10")
    assert dia.has_entity("ent11")

def test_dia_rename_multiple_entities():
    dia = Diagram()
    dia.add_entity("ent1")
    dia.add_entity("ent2")
    assert dia.has_entity("ent1")
    assert dia.has_entity("ent2")
    assert not dia.has_entity("ent3")
    assert not dia.has_entity("ent4")
    dia.rename_entity("ent1", "ent3")
    dia.rename_entity("ent2", "ent4")
    assert not dia.has_entity("ent1")
    assert not dia.has_entity("ent2")
    assert dia.has_entity("ent3")
    assert dia.has_entity("ent4")


def test_dia_add_relation():
    dia = Diagram()
    dia.add_entity("ent1")
    dia.add_entity("ent2")
    assert len(dia._relations) == 0
    dia.add_relation("ent1", "ent2", "aggregation")
    assert len(dia._relations) == 1

def test_dia_delete_relation():
    dia = Diagram()
    dia.add_entity("ent1")
    dia.add_entity("ent2")
    dia.add_relation("ent1", "ent2", "aggregation")
    assert len(dia._relations) == 1
    dia.delete_relation("ent1", "ent2")
    assert len(dia._relations) == 0
    