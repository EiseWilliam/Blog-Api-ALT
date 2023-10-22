import re
import unicodedata


def slugify(string):

    """
    Slugify a unicode string.

    Example:

        >>> slugify(u"Héllø Wörld")
        u"hello-world"

    """

    return re.sub(r'[-\s]+', '-',
            str(
                re.sub(r'[^\w\s-]', '',
                    unicodedata.normalize('NFKD', string)
                    .encode('ascii', 'ignore')
                    .decode())
                .strip()
                .lower()))


async def unique_slug_id(title: str, Collection) -> str:
    """
    This function returns a slug that is unique to the database,
    it attaches a unique number to the slug if there is another article with same title
    """
    slug = slugify(title)
    # Check if the slug already exists in the database
    matches: int =  Article.count_documents({"slug": slug})
    if matches > 0:
        # Append a number to the end of the slug until it is unique
        count = 1
        while True:
            new_slug = f"{slug}-{count}"
            # Check if the new slug exists
            matches = Article.count_documents({"slug": new_slug})
            if matches == 0:
                return new_slug
            count += 1
    else:
        return slug
