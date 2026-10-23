"""Employee Management System - simple CLI app with JSON storage."""

import json
import os
from dataclasses import dataclass, asdict

DATA_FILE = "employees.json"


@dataclass
class Employee:
    emp_id: int
    name: str
    position: str
    department: str
    salary: float


class EmployeeManager:
    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.employees = {}
        self.load()

    # ---------- storage ----------
    def load(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                for item in json.load(f):
                    emp = Employee(**item)
                    self.employees[emp.emp_id] = emp
        except (json.JSONDecodeError, TypeError):
            print("Warning: data file is corrupted. Starting empty.")

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([asdict(e) for e in self.employees.values()], f, indent=2)

    # ---------- operations ----------
    def next_id(self):
        return max(self.employees, default=0) + 1

    def add(self, name, position, department, salary):
        emp = Employee(self.next_id(), name, position, department, salary)
        self.employees[emp.emp_id] = emp
        self.save()
        return emp

    def update(self, emp_id, **fields):
        emp = self.employees.get(emp_id)
        if not emp:
            return None
        for key, value in fields.items():
            if value not in (None, ""):
                setattr(emp, key, value)
        self.save()
        return emp

    def delete(self, emp_id):
        emp = self.employees.pop(emp_id, None)
        if emp:
            self.save()
        return emp

    def search(self, keyword):
        keyword = keyword.lower()
        return [
            e for e in self.employees.values()
            if keyword in e.name.lower()
            or keyword in e.position.lower()
            or keyword in e.department.lower()
        ]

    def report(self):
        if not self.employees:
            return None
        salaries = [e.salary for e in self.employees.values()]
        by_dept = {}
        for e in self.employees.values():
            by_dept[e.department] = by_dept.get(e.department, 0) + 1
        return {
            "total": len(salaries),
            "payroll": sum(salaries),
            "average": sum(salaries) / len(salaries),
            "by_department": by_dept,
        }


# ---------- helpers for the CLI ----------
def print_table(employees):
    if not employees:
        print("No employees found.")
        return
    print(f"\n{'ID':<5}{'Name':<22}{'Position':<22}{'Department':<16}{'Salary':>10}")
    print("-" * 75)
    for e in sorted(employees, key=lambda x: x.emp_id):
        print(f"{e.emp_id:<5}{e.name:<22}{e.position:<22}{e.department:<16}{e.salary:>10,.2f}")
    print()


def ask_float(prompt, allow_blank=False):
    while True:
        raw = input(prompt).strip()
        if allow_blank and raw == "":
            return None
        try:
            value = float(raw)
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a valid positive number.")


def ask_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Please enter a valid whole number.")


def ask_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


MENU = """
===== Employee Management =====
1. Add employee
2. View all employees
3. Search employees
4. Update employee
5. Delete employee
6. Report
0. Exit
"""


def main():
    manager = EmployeeManager()

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = ask_text("Name: ")
            position = ask_text("Position: ")
            department = ask_text("Department: ")
            salary = ask_float("Salary: ")
            emp = manager.add(name, position, department, salary)
            print(f"Added {emp.name} with ID {emp.emp_id}.")

        elif choice == "2":
            print_table(list(manager.employees.values()))

        elif choice == "3":
            keyword = ask_text("Search (name/position/department): ")
            print_table(manager.search(keyword))

        elif choice == "4":
            emp_id = ask_int("Employee ID to update: ")
            if emp_id not in manager.employees:
                print("Employee not found.")
                continue
            print("Leave a field blank to keep its current value.")
            name = input("New name: ").strip()
            position = input("New position: ").strip()
            department = input("New department: ").strip()
            salary = ask_float("New salary: ", allow_blank=True)
            manager.update(emp_id, name=name, position=position,
                           department=department, salary=salary)
            print("Employee updated.")

        elif choice == "5":
            emp_id = ask_int("Employee ID to delete: ")
            emp = manager.employees.get(emp_id)
            if not emp:
                print("Employee not found.")
            elif input(f"Delete {emp.name}? (y/n): ").lower() == "y":
                manager.delete(emp_id)
                print("Employee deleted.")

        elif choice == "6":
            data = manager.report()
            if not data:
                print("No data yet.")
            else:
                print(f"\nTotal employees: {data['total']}")
                print(f"Total payroll:   {data['payroll']:,.2f}")
                print(f"Average salary:  {data['average']:,.2f}")
                print("By department:")
                for dept, count in data["by_department"].items():
                    print(f"  - {dept}: {count}")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()