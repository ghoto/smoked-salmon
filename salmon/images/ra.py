import requests

from salmon import config
from salmon.errors import ImageUploadFailed
from salmon.images.base import BaseImageUploader


class ImageUploader(BaseImageUploader):
    def _perform(self, file_, ext):
        url = "https://thesungod.xyz/api/image/upload"
        data = {'api_key': config.RA_KEY}
        files = {'image': file_}
        headers = {}

        resp = requests.post(url, headers=headers, data=data, files=files)

        if resp.status_code == requests.codes.ok:
            try:
                # Parse the JSON response to get the list of image links
                json_data = resp.json()
                image_links = json_data.get('links')
                
                # Check if smoked-salmon received at least one link
                if image_links and isinstance(image_links, list) and len(image_links) > 0:
                    # Return the first image URL and None for the deletion URL
                    return image_links[0], None
                else:
                    raise ValueError("No image links found in the response")
            except (ValueError, KeyError) as e:
                raise ImageUploadFailed(
                    f"Failed decoding body or invalid JSON structure:\n{e}\n{resp.content}"
                ) from e
        else:
            raise ImageUploadFailed(
                f"Failed. Status {resp.status_code}:\n{resp.content}"
            )
