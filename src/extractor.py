import re
from bs4 import BeautifulSoup


class DataExtractor:

    def __init__(self, driver):
        self.driver = driver

    def extract_current_post(self):

        html = self.driver.execute_script(
            "return document.body.innerHTML;"
        )

        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text("\n", strip=True)
        with open("debug.txt", "w", encoding="utf-8") as f :
            f.write(text)
        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        # Keep only the last section, which contains the opened popup
        lines = lines[-25:]
        for line in lines :
            with open("debug.txt", "w", encoding="utf-8") as f :
                f.write(line)
        data = {
            "username": "",
            "title": "",
            "price": None,
            "likes": 0,
            "comments": 0,
            "caption": ""
        }

        # Username
        for line in lines:
            if "_" in line and len(line) < 50:
                data["username"] = line
                break

        # Likes
        for i, line in enumerate(lines):
            if line == "لایک" and i > 0:
                try:
                    data["likes"] = int(
                        re.sub(r"\D", "", lines[i - 1])
                    )
                except:
                    pass

        # Comments
        for line in lines:
            m = re.search(r"مشاهده ی\s+(\d+)\s+کامنت", line)

            if m:
                data["comments"] = int(m.group(1))
                break

        # Price
        for line in lines:
            if "قیمت" in line:

                data["price"] = line

                numbers = re.search(
                    r"(\d[\d,]*)",
                    line
                )

                if numbers:
                    data["price_number"] = int(
                        numbers.group(1).replace(",", "")
                    )

                break

        # Product title
        for line in lines:

            if "بنام" in line:

                data["title"] = (
                    line.replace("بنام", "")
                        .replace(":", "")
                        .strip()
                )

                break
            elif "ننام" in line:

                data["title"] = (
                    line.replace("ننام", "")
                        .replace(":", "")
                        .strip()
                )

                break
            elif "نام" in line :

                data["title"] = (
                    line.replace("نام", "")
                        .replace(":", "")
                        .strip()
                )

                break

        # Full caption
        start = -1

        for i, line in enumerate(lines):

            if "بنام" in line or "ننام" in line or "نام" in line:
                start = i
                break

        if start != -1:

            end = len(lines)

            for i in range(start, len(lines)):

                if "روز پیش" in lines[i]:
                    end = i
                    break

            data["caption"] = "\n".join(
                lines[start:end]
            )

        return data