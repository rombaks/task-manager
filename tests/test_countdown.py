import time
import pathlib

import pytest
from django.test import override_settings

from rest_framework import status

from tests.base_test_views import TestViewSetBase


class TestCountdownJob(TestViewSetBase):
    basename = "countdown"
    COUNTDOWN_TIME = 5
    DELAY = 2

    def test_countdown_machinery(self):
        response = self.request_create({"seconds": self.COUNTDOWN_TIME})
        assert response.status_code == status.HTTP_201_CREATED

        job_location = response.headers["Location"]
        start = time.monotonic()
        while response.data.get("status") != "success":
            assert (
                time.monotonic() < start + self.COUNTDOWN_TIME + self.DELAY
            ), "Time out"
            response = self.client.get(job_location)

        assert time.monotonic() > start + self.COUNTDOWN_TIME
        file_name = response.headers["Location"].split("/", 3)[-1]
        file = pathlib.Path(file_name)
        assert file.is_file()
        assert file.read_bytes() == b"test data"
        file.unlink(missing_ok=True)
