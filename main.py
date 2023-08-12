import tidalapi
import xml.etree.ElementTree as ET
from typing import List


def store_session(token_type, access_token, refresh_token, expiry_token):
    with open("./files/session.cfg", "w") as cfg:
        cfg.write(str(token_type) + "\n")
        cfg.write(str(access_token) + "\n")
        cfg.write(str(refresh_token) + "\n")
        cfg.write(str(expiry_token) + "\n")


def read_session():
    with open("./files/session.cfg", "r") as cfg:
        lines = cfg.readlines()
        new_lines = []
        for line in lines:
            new_lines.append(line.strip())
        return new_lines


def parse_wmp(file_path: str) -> List[str]:
    tree = ET.parse(file_path)
    root = tree.getroot()
    songs: List[str] = []
    for child in root[1][0]:
        src = child.attrib["src"]
        song_incl_ext = src.split("\\")[-1]
        song = song_incl_ext.rstrip(".mp3")
        songs.append(song)
    return songs


def main():
    # The function is print by default, but you can use anything, here we do it to avoid the print being swallowed
    session = tidalapi.Session()
    local_sess = read_session()
    if not local_sess:
        session.login_oauth_simple()
        print(session.check_login())
        token_type = session.token_type
        access_token = session.access_token
        refresh_token = session.refresh_token # Not needed if you don't care about refreshing
        expiry_time = session.expiry_time
        store_session(token_type, access_token, refresh_token, expiry_time)
    else:
        token_type = local_sess[0]
        access_token = local_sess[1]
        refresh_token = local_sess[2]
        expiry_time = local_sess[3]

    login_success = session.load_oauth_session(token_type, access_token, refresh_token, expiry_time)
    if not login_success:
        session.login_oauth_simple()
        print(session.check_login())
        token_type = session.token_type
        access_token = session.access_token
        refresh_token = session.refresh_token # Not needed if you don't care about refreshing
        expiry_time = session.expiry_time
        store_session(token_type, access_token, refresh_token, expiry_time)

    playlist = "(L)"
    playlist_filepath = f"./data/{playlist}.wpl"
    songs = parse_wmp(playlist_filepath)

    for song in songs:
        print("\n" + song)
        tidal_results = session.search(song)
        print(tidal_results)
    # session.user.playlist.create_playlist(playlist)

if __name__ == "__main__":
    main()
