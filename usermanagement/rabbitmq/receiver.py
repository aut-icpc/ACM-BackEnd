# import pika, json, datetime, time
# from . import startup
# from usermanagement.utils import send_mail as sendMail


# connection, channel = startup.start()

# # Using a class because a single global variable would cause problems with python in this case.
# # I've been using global variables my entire life and I still can't figure out why.

# class state:
#     MAILING_LIMIT = 95
#     mails_left = MAILING_LIMIT


# def seconds_until_end_of_day(dt=None):
#     if dt is None:
#         dt = datetime.datetime.now()
#     return ((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)
    

# def send_email(ch, method, properties, body):
#     email_dict = json.loads(body)
#     if state.mails_left > 1:
#         try:
#             sendMail(**email_dict)
#             state.mails_left -= 1
#         except Exception as ex:
#             print(ex)
#     else:
#         waiting_seconds = seconds_until_end_of_day()
#         time.sleep(waiting_seconds)
#         sendMail(**email_dict)
#         state.mails_left = state.MAILING_LIMIT
#     ch.basic_ack(
#         delivery_tag = method.delivery_tag
#     )


# channel.basic_consume(
#     queue = startup.QUEUE_NAME,
#     on_message_callback = send_email,
#     auto_ack = False
# )
