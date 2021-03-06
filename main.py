import logging, argparse, sys, ssl

from aiogram.dispatcher.webhook import *
from aiogram.utils.executor import start_polling, start_webhook

from bot.dispathcer import dp
from bot.filters import *
from bot.handlers import *

logging.basicConfig(level=logging.ERROR, filename="error_logs.txt")

# region Argument parser
# Arguments config
parser = argparse.ArgumentParser("Telegram bot by D33")
parser.add_argument('--sock', help='UNIX Socket path')
parser.add_argument('--host', help='Webserver host')
parser.add_argument('--port', type=int, help='Webserver port')
parser.add_argument('--cert', help='Path to SSL certificate')
parser.add_argument('--pkey', help='Path to SSL private key')
parser.add_argument('--host-name', help='Set webhook host name')
parser.add_argument('--webhook-port', type=int, help='Port for webhook (default=port)')
parser.add_argument('--webhook-path', default='/webhook', help='Port for webhook (default=port)')
# endregion


async def on_startup(dispatcher, url=None, cert=None):
    bot = dispatcher.bot

    # Get current webhook status
    webhook = await bot.get_webhook_info()

    if url:
        # If URL is bad
        if webhook.url != url:
            # If URL doesnt match with by current remove webhook
            if not webhook.url:
                await bot.delete_webhook()

            # Set new URL for webhook
            if cert:
                with open(cert, 'rb') as cert_file:
                    await bot.set_webhook(url, certificate=cert_file)
            else:
                await bot.set_webhook(url)
    elif webhook.url:
        # Otherwise remove webhook.
        await bot.delete_webhook()


async def on_shutdown(dispatcher):
    print('Shutdown.')


def main(arguments):
    args = parser.parse_args(arguments)
    sock = args.sock
    host = args.host
    port = args.port
    cert = args.cert
    pkey = args.pkey
    host_name = args.host_name or host
    webhook_port = args.webhook_port or port
    webhook_path = args.webhook_path

    # Fi webhook path
    if not webhook_path.startswith('/'):
        webhook_path = '/' + webhook_path

    # Generate webhook URL
    webhook_url = f"https://{host_name}:{webhook_port}{webhook_path}"

    # Create bot & dispatcher instances.
    dispatcher = dp

    if (sock or host) and host_name:
        if cert and pkey:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.load_cert_chain(cert, pkey)
        else:
            ssl_context = None

        start_webhook(dispatcher, webhook_path,
                      on_startup=functools.partial(on_startup, url=webhook_url, cert=cert),
                      on_shutdown=on_shutdown,
                      host=host, port=port, path=sock, ssl_context=ssl_context)
    else:
        start_polling(dispatcher, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == "__main__":
    argv = sys.argv[1:]

    main(argv)