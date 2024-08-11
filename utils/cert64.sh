echo "The key is"
cat webhook.key | base64 | tr -d '\n'
echo
echo "The cert is"
cat webhook.crt | base64 | tr -d '\n'
echo