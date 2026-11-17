"""Notifications (mocked).

No real email is sent. MockNotificationService stands in for a real email
provider (see https://en.wikipedia.org/wiki/Mock_object): it records every
message in memory and appends it to outbox.txt so behaviour can be inspected.
Swap it for a real implementation by replacing `notifier`.
"""


class MockNotificationService:
    def __init__(self, outbox_path="outbox.txt"):
        self.outbox_path = outbox_path
        self.sent = []  # in-memory record, handy for tests

    def send(self, to, subject, body):
        self.sent.append({"to": to, "subject": subject, "body": body})
        with open(self.outbox_path, "a") as f:
            f.write("TO: " + to + " | SUBJECT: " + subject + " | BODY: " + body + "\n")

    def checkout(self, email, title):
        self.send(email, "Book checked out", "You checked out " + title)

    def renewal(self, email, title):
        self.send(email, "Loan renewed", "You renewed " + title)

    def returned(self, email, title, fine):
        self.send(email, "Book returned", "You returned " + title + ". Fine: $" + str(fine))

    def fine_paid(self, email, amount):
        self.send(email, "Fine paid", "We received $" + str(amount))


notifier = MockNotificationService()
