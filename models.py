"""
Data models for Library Management System
Defines core classes for Book, Member, and BorrowRecord
"""

from datetime import datetime, timedelta
from typing import Optional


class Book:
    """Represents a book in the library"""
    
    def __init__(self, book_id: str, title: str, author: str, isbn: str, 
                 copies: int = 1, publication_year: int = 2024):
        """
        Initialize a Book object
        
        Args:
            book_id: Unique identifier for the book
            title: Title of the book
            author: Author name
            isbn: ISBN number
            copies: Number of copies available
            publication_year: Year of publication
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_copies = copies
        self.available_copies = copies
        self.publication_year = publication_year
    
    def issue_book(self) -> bool:
        """Issue a book if available"""
        if self.available_copies > 0:
            self.available_copies -= 1
            return True
        return False
    
    def return_book(self) -> bool:
        """Return a book"""
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            return True
        return False
    
    def __str__(self) -> str:
        return f"Book(ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Available: {self.available_copies}/{self.total_copies})"


class Member:
    """Represents a library member"""
    
    def __init__(self, member_id: str, name: str, email: str, phone: str):
        """
        Initialize a Member object
        
        Args:
            member_id: Unique identifier for the member
            name: Member's full name
            email: Member's email address
            phone: Member's phone number
        """
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.membership_date = datetime.now()
        self.is_active = True
        self.borrowed_books = []  # List of book_ids currently borrowed
        self.total_fine = 0.0
    
    def __str__(self) -> str:
        return f"Member(ID: {self.member_id}, Name: {self.name}, Email: {self.email}, Borrowed: {len(self.borrowed_books)})"


class BorrowRecord:
    """Represents a borrowing transaction"""
    
    BORROWING_PERIOD_DAYS = 14
    FINE_PER_DAY = 5.0  # Fine in currency units
    
    def __init__(self, record_id: str, book_id: str, member_id: str):
        """
        Initialize a BorrowRecord object
        
        Args:
            record_id: Unique identifier for the record
            book_id: ID of the borrowed book
            member_id: ID of the member who borrowed
        """
        self.record_id = record_id
        self.book_id = book_id
        self.member_id = member_id
        self.issue_date = datetime.now()
        self.due_date = self.issue_date + timedelta(days=self.BORROWING_PERIOD_DAYS)
        self.return_date: Optional[datetime] = None
        self.fine_amount = 0.0
        self.is_active = True
    
    def calculate_fine(self) -> float:
        """Calculate fine if book is returned late"""
        if self.return_date:
            if self.return_date > self.due_date:
                overdue_days = (self.return_date - self.due_date).days
                self.fine_amount = overdue_days * self.FINE_PER_DAY
        return self.fine_amount
    
    def is_overdue(self) -> bool:
        """Check if the borrowed book is overdue"""
        if self.is_active:
            return datetime.now() > self.due_date
        return False
    
    def get_overdue_days(self) -> int:
        """Get number of days overdue"""
        if self.is_active and self.is_overdue():
            return (datetime.now() - self.due_date).days
        return 0
    
    def __str__(self) -> str:
        status = "Active" if self.is_active else "Returned"
        return f"BorrowRecord(ID: {self.record_id}, Book: {self.book_id}, Member: {self.member_id}, Status: {status}, Due: {self.due_date.date()})"
