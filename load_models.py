import time
import torch

from recognize_anything.ram.models import ram_plus
from recognize_anything.ram.models import ram
from recognize_anything.ram.models import tag2text

from recognize_anything.ram import inference_ram
from recognize_anything.ram import inference_tag2text
from recognize_anything.ram import get_transform


def load_ram_plus(image_size):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print("Using device: ", device)

    transform = get_transform(image_size=image_size)

    model = ram_plus(pretrained="/data/pretrained/ram_plus_swin_large_14m.pth",
                     image_size=image_size,
                     vit='swin_l')

    model.eval()
    model = model.to(device)

    print("Loaded ram_plus_swin_large_14m.pth")

    def inference(image):
        start_time = time.perf_counter()

        transformed = transform(image).unsqueeze(0).to(device)
        result = inference_ram(transformed, model)

        print(f"processed image in {time.perf_counter() - start_time:0.4f}s")

        return {
            "english": result[0].split(" | "),
            "chinese": result[1].split(" | ")
        }

    return {
        "device": device,
        "model": model,
        "inference": inference,
        "transform": transform
    }


def load_ram(image_size):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print("Using device: ", device)

    transform = get_transform(image_size=image_size)

    model = ram(pretrained="/data/pretrained/ram_swin_large_14m.pth",
                image_size=image_size,
                vit='swin_l')
    model.eval()
    model = model.to(device)

    print("Loaded ram_swin_large_14m.pth")

    def inference(image):
        start_time = time.perf_counter()

        transformed = transform(image).unsqueeze(0).to(device)
        result = inference_ram(transformed, model)

        print(f"processed image in {time.perf_counter() - start_time:0.4f}s")

        return {
            "english": result[0].split(" | "),
            "chinese": result[1].split(" | ")
        }

    return {
        "device": device,
        "model": model,
        "inference": inference,
        "transform": transform
    }


def load_tag2text(image_size, threshold=0.68, delete_tag_index=None):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print("Using device: ", device)

    transform = get_transform(image_size=image_size)

    # delete some tags that may disturb captioning
    # 127: "quarter"; 2961: "back", 3351: "two"; 3265: "three"; 3338: "four"; 3355: "five"; 3359: "one"

    model = tag2text(pretrained="/data/pretrained/tag2text_swin_14m.pth",
                     image_size=image_size,
                     vit='swin_b',
                     delete_tag_index=(delete_tag_index or [127, 2961, 3351, 3265, 3338, 3355, 3359]))
    model.threshold = threshold
    model.eval()
    model = model.to(device)

    print("Loaded tag2text_swin_14m.pth")

    def inference(image):
        start_time = time.perf_counter()

        transformed = transform(image).unsqueeze(0).to(device)
        result = inference_tag2text(transformed, model)

        print(f"processed image in {time.perf_counter() - start_time:0.4f}s")

        return {
            "model_tags": result[0] and result[0].split(" | "),
            "user_tags": result[1] and result[1].split(" | "),
            "image_caption": result[2]
        }

    return {
        "device": device,
        "model": model,
        "inference": inference,
        "transform": transform
    }


def load_model(model_name, image_size, threshold, delete_tag_index):
    print("Loading model: ", model_name)
    match model_name:
        case "ram_plus":
            return load_ram_plus(image_size)
        case "ram":
            return load_ram(image_size)
        case "tag2text":
            # TODO: pass threshold / delete_tag_index parameters
            return load_tag2text(image_size, threshold, delete_tag_index)
