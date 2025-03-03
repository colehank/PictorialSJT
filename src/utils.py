import json
import re
from PIL import Image, ImageOps
import re


def extract_json(text: str) -> dict:
    """
    Extract JSON from a string.

    Parameters:
    -----------
    text: str
        The string to extract JSON from.

    Returns:
    --------
    data: dict
        The extracted JSON data.
    """
    if "```json" in text:
        text = re.sub(r"```json", "", text)  # 移除 ```json
    if "```" in text:
        text = re.sub(r"```", "", text)

    text = text.replace(r"\n", "\n")  # 还原 \n 为换行符

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def make_sequence(image_list, border_width=10, border_color="white"):
    """
    Concatenate images horizontally.

    Parameters:
    -----------
    image_list: list
        A list of images to concatenate.
    border_width: int
        The width of the border.
    border_color: str
        The color of the border.

    Returns:
    --------
    new_im: Image
        The concatenated image.
    """
    bordered_images = [
        ImageOps.expand(im, border=border_width, fill=border_color) for im in image_list
    ]

    total_width = sum(im.width for im in bordered_images)
    max_height = max(im.height for im in bordered_images)

    new_im = Image.new("RGBA", (total_width, max_height), border_color)

    x_offset = 0
    for im in bordered_images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.width

    return new_im


def parse_variables(template: str, variables: dict) -> str:
    """
    将字符串中的变量表达式（如 `var[index]`）替换为实际值。

    参数:
        template (str): 包含变量表达式的原始字符串。
        variables (dict): 变量字典，包含所有可能用到的变量名及其值。

    返回:
        str: 替换后的字符串。

    示例:
        >>> characters = ['you', 'friend']
        >>> parse_variables('characters[0] on a tram with characters[1]', {'characters': characters})
        'you on a tram with friend'

        >>> data = {'name': 'Alice', 'scores': [90, 85]}
        >>> parse_variables("data['name']'s score is data['scores'][0]", {'data': data})
        "Alice's score is 90"
    """
    # 匹配类似 var[...] 的表达式，支持数字、字符串（单/双引号）及嵌套结构
    pattern = re.compile(r'(\w+)((?:\[(?:".*?"|\'.*?\'|\d+)\])+)')

    def replacer(match):
        var_name = match.group(1)
        indices_str = match.group(2)
        if var_name not in variables:
            return match.group(0)  # 变量不存在则保留原表达式

        # 解析索引部分，例如 "[0][1]['key']" -> [0, 1, 'key']
        indices = []
        index_matches = re.finditer(r'\[(".*?"|\'.*?\'|\d+)\]', indices_str)
        for m in index_matches:
            index = m.group(1).strip("'\"")
            # 尝试将索引转换为整数（如果是数字）
            index = int(index) if index.isdigit() else index
            indices.append(index)

        # 逐层获取值
        try:
            value = variables[var_name]
            for idx in indices:
                value = value[idx]
            return str(value)
        except (KeyError, IndexError, TypeError):
            return match.group(0)  # 索引无效则保留原表达式

    return pattern.sub(replacer, template)
