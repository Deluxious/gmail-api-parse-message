import base64


def index_headers(headers):
    return {h["name"]: h["value"] for h in headers}


def decode_content(data):
    return base64.urlsafe_b64decode(data).decode("utf-8")


def parse_gmail_message(response):
    result = {
        "id": response["id"],
        "thread_id": response["threadId"],
        "label_ids": response["labelIds"],
        "snippet": response["snippet"],
        "history_id": response["historyId"],
    }

    if "internalDate" in response:
        result["internal_date"] = int(response["internalDate"])

    payload = response["payload"]
    if not payload:
        return result

    headers = index_headers(payload["headers"])
    result["headers"] = headers
    parts = [payload]
    first_part_processed = False

    while parts:
        part = parts.pop(0)
        if "parts" in part:
            parts.extend(part["parts"])
        if first_part_processed:
            headers = index_headers(part["headers"])
        if not part["body"]:
            continue

        is_html = "mimeType" in part and "text/html" in part["mimeType"]
        is_plain = "mimeType" in part and "text/plain" in part["mimeType"]
        is_attachment = (
            "content_disposition" in headers
            and "attachment" in headers["content_disposition"]
        )
        is_inline = (
            "content_disposition" in headers
            and "inline" in headers["content_disposition"]
        )
        if is_html and not is_attachment:
            result["text_html"] = decode_content(part["body"]["data"])
        elif is_plain and not is_attachment:
            result["text_plain"] = decode_content(part["body"]["data"])
        elif is_attachment:
            body = part["body"]
            if not result["attachments"]:
                result["attachments"] = []
            result["attachments"].append(
                {
                    "filename": part["filename"],
                    "mime_type": part["mimeType"],
                    "size": body.size,
                    "attachment_id": body.attachment_id,
                    "headers": index_headers(part["headers"]),
                }
            )
        elif is_inline:
            body = part["body"]
            if not result["inline"]:
                result["inline"] = []
            result["inline"].append(
                {
                    "filename": part["filename"],
                    "mime_type": part["mimeType"],
                    "size": body["size"],
                    "attachment_id": body["attachment_id"],
                    "headers": index_headers(part["headers"]),
                }
            )

        first_part_processed = True

    return result

