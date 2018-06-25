import pytest
from flask import url_for
from app import app, db
from app.models import User, Post
from test_live_server import TestLiveServer


class TestAnonymousUser(TestLiveServer):
    def test_no_posts_no_user(self, client):
        client.browser.get(client.get_server_url())
        self.wait_for_element(client, "page-title", "Wolfit")
        assert "Wolfit" in client.browser.title
        greeting = client.browser.find_element_by_id("user-greeting").text
        assert "Anonymous" in greeting

    def test_navigation_when_not_logged_in(self, client):
        client.browser.get(client.get_server_url())
        self.wait_for_element(client, "page-title", "Wolfit")
        nav = client.browser.find_element_by_id("nav-home").find_element_by_xpath(
            ".//a"
        )
        assert "index" in nav.get_attribute("href")
        nav = client.browser.find_element_by_id("nav-login").find_element_by_xpath(
            ".//a"
        )
        assert "login" in nav.get_attribute("href")

    def test_single_post_should_have_link_back_to_author(self, client, single_post):
        client.browser.get(client.get_server_url())
        self.wait_for_element(client, "page-title", "Wolfit")
        post_link = client.browser.find_element_by_id("post-0-link")
        post_link.click()
        self.wait_for_element(client, "page-title", single_post.title)
        author_link = client.browser.find_element_by_id("author-link")
        assert single_post.author.username in author_link.text
