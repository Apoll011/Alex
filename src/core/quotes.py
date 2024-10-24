"""
PyQuotes - A simple Python module for inspirational quotes
"""

import random

class PyQuotes:
    def __init__(self):
        self.quotes = {
            'success': [
                "The only way to do great work is to love what you do. - Steve Jobs",
                "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
                "The secret of success is to do the common thing uncommonly well. - John D. Rockefeller Jr.",
                "I find that the harder I work, the more luck I seem to have. - Thomas Jefferson",
            ],
            'motivation': [
                "Believe you can and you're halfway there. - Theodore Roosevelt",
                "It does not matter how slowly you go as long as you do not stop. - Confucius",
                "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
                "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
            ],
            'wisdom': [
                "The only true wisdom is in knowing you know nothing. - Socrates",
                "The journey of a thousand miles begins with one step. - Lao Tzu",
                "Yesterday I was clever, so I wanted to change the world. Today I am wise, so I am changing myself. - Rumi",
                "The only way to do great work is to love what you do. - Steve Jobs",
            ],
            'life': [
                "Life is what happens to you while you're busy making other plans. - John Lennon",
                "The purpose of our lives is to be happy. - Dalai Lama",
                "Life is really simple, but we insist on making it complicated. - Confucius",
                "In the end, it's not the years in your life that count. It's the life in your years. - Abraham Lincoln",
            ]
        }
        self.all_quotes = [quote for category in self.quotes.values() for quote in category]

    def get_quote(self, category=None):
        """
        Get a random quote, optionally from a specific category.
        
        :param category: Optional category to choose from ('success', 'motivation', 'wisdom', 'life')
        :return: A random quote as a string
        """
        if category and category in self.quotes:
            return random.choice(self.quotes[category])
        return random.choice(self.all_quotes)

    def get_clean_quote(self, category=None):
        return self.get_quote(category).replace(" - ", " by ").replace(":", ",")

    def get_categories(self):
        """
        Get the list of available categories.
        
        :return: List of category names
        """
        return list(self.quotes.keys())