from translation import compile_translations
from update_content import deploy_update_content


if __name__ == "__main__":
    # Compile translations
    compile_translations()

    # Deploy content updates
    deploy_update_content()
