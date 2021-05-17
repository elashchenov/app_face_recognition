from config.config import __version__

# main link for rest api
main_link = f"/database/{__version__}"


add_device = f"{main_link}/add-device/<device_name>"

add_user = f"{main_link}/add-user"

login = f"{main_link}/login"

get_status_train = f"{main_link}/get-status-train"

update_user = f"{main_link}/update-user"

add_photo = f"{main_link}/add-photo"

set_percent = f"{main_link}/set-percent/<percent>/<id_user>"

check_user = f"{main_link}/check-user/<email>"

add_item_journal = f"{main_link}/add-journal"

delete_user = f"{main_link}/delete-user/<email>"

