echo "Running github-tokens script"

if [ "${GITHUB_TOKEN}" != "" ]; then

    if [ -z "${GITHUB_HOST}" ]; then
        GITHUB_HOST=github.com
    fi

    git config --global --replace-all user.email "${GITHUB_EMAIL}"
    git config --global --replace-all user.name "${GITHUB_NAME}"
    git config --global --replace-all user.ghtoken "${GITHUB_TOKEN}"
    git config --global --replace-all push.default simple
    git config --global --replace-all url."https://${GITHUB_USER}:${GITHUB_TOKEN}@${GITHUB_HOST}".insteadOf "https://${GITHUB_HOST}"
    git config --global --replace-all url."https://${GITHUB_USER}:${GITHUB_TOKEN}@${GITHUB_HOST}/".insteadOf "git@${GITHUB_HOST}:"
fi

