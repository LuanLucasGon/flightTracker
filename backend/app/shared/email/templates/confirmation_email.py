def build_confirmation_email(name: str, confirmation_url: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Confirme seu email — Flight Tracker</title>
    </head>
    <body style="margin:0;padding:0;background-color:#0A0A0F;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0A0A0F;padding:40px 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color:#12121A;border-radius:16px;border:1px solid #2A2A3A;overflow:hidden;">

                        <!-- Header -->
                        <tr>
                            <td style="background:linear-gradient(135deg,#1A1A28 0%,#12121A 100%);padding:40px;text-align:center;border-bottom:1px solid #2A2A3A;">
                                <div style="display:inline-flex;align-items:center;gap:10px;">
                                    <span style="font-size:24px;">✈️</span>
                                    <span style="color:#F0F0FF;font-size:22px;font-weight:700;letter-spacing:-0.5px;">Flight Tracker</span>
                                </div>
                            </td>
                        </tr>

                        <!-- Body -->
                        <tr>
                            <td style="padding:48px 40px;">
                                <h1 style="color:#F0F0FF;font-size:28px;font-weight:700;margin:0 0 12px;letter-spacing:-0.5px;">
                                    Confirme seu email
                                </h1>
                                <p style="color:#8888AA;font-size:16px;line-height:1.6;margin:0 0 32px;">
                                    Olá{f', {name}' if name else ''}! Para continuar seu cadastro no Flight Tracker,
                                    confirme seu endereço de email clicando no botão abaixo.
                                </p>

                                <!-- CTA Button -->
                                <table cellpadding="0" cellspacing="0" style="margin:0 0 32px;">
                                    <tr>
                                        <td style="background-color:#2D7EFF;border-radius:10px;">
                                            <a href="{confirmation_url}"
                                               style="display:inline-block;padding:16px 40px;color:#FFFFFF;font-size:16px;font-weight:600;text-decoration:none;letter-spacing:-0.2px;">
                                                Confirmar email →
                                            </a>
                                        </td>
                                    </tr>
                                </table>

                                <p style="color:#8888AA;font-size:14px;line-height:1.6;margin:0 0 8px;">
                                    Se o botão não funcionar, copie e cole o link abaixo no seu navegador:
                                </p>
                                <p style="margin:0;">
                                    <a href="{confirmation_url}"
                                       style="color:#2D7EFF;font-size:13px;word-break:break-all;text-decoration:none;">
                                        {confirmation_url}
                                    </a>
                                </p>
                            </td>
                        </tr>

                        <!-- Footer -->
                        <tr>
                            <td style="padding:24px 40px;border-top:1px solid #2A2A3A;text-align:center;">
                                <p style="color:#8888AA;font-size:13px;margin:0 0 8px;">
                                    Este link expira em <strong style="color:#F0F0FF;">24 horas</strong>.
                                </p>
                                <p style="color:#8888AA;font-size:12px;margin:0;">
                                    Se você não criou uma conta no Flight Tracker, ignore este email.
                                </p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """