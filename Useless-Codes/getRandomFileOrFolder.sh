# Usage  :  ./random.sh "path" 'amount?' -type?
# Example:  ./random.sh "/home/lynnux/Downloads" '2' -file

# Function to get random folders
get_random_folders() {
  local path="$1"
  local amount="$2"
  find "$path" -mindepth 1 -maxdepth 1 -type d | shuf -n "$amount"
}

# Function to get random files
get_random_files() {
  local path="$1"
  local amount="$2"
  find "$path" -type f | shuf -n "$amount"
}

# Main script
path="$1"
amount="${2:-1}"
type="${3:-folder}"

# Validate path
if [ ! -d "$path" ]; then
  echo "Invalid path: $path"
  exit 1
fi

# Determine type and call appropriate function
case "$type" in
  -file)
    get_random_files "$path" "$amount"
    ;;
  -folder)
    get_random_folders "$path" "$amount"
    ;;
  *)
    get_random_folders "$path" "$amount"
    ;;
esac
