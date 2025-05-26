case $SHELL in
    "/bin/bash")
        echo -e "alias rcp=\"python3 recipe.py\"" >> ~/.bashrc
    ;;

    "/bin/zsh")
        echo -e "alias rcp=\"python3 recipe.py\"" >> ~/.zshrc
    ;;
esac
