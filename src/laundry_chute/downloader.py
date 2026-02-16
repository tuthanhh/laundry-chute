import io
import os

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from tqdm import tqdm


class DriveDownloader:
    def __init__(self, key_file):
        SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
        creds = Credentials.from_service_account_file(key_file, scopes=SCOPES)
        self.service = build("drive", "v3", credentials=creds)
        self.root_id = "1NiZ9rL19qKLqt0uNcP5tIqc0fUrksAPs"

    def get_folder_id(
        self, root_id: str, version: str, song_name: str, variant: str | None = None
    ) -> str:
        """
        Finds the ID of a song folder located inside a specific version folder.
        Structure: [Root] -> [Version Folder] -> [Song Folder]
        """
        print(f"Hunting for '{song_name}' inside '{version}'...")

        # Manual mapping for special case:
        if version == "maimaiでらっくす":
            version = "DX"
        if version == "maimaiでらっくす PLUS":
            version = "DX PLUS"

        # Replacement for apostrophe
        song_name = song_name.replace("'", "\\'")
        
        # Find the Version Folder (e.g., "PRiSM/ FESTiVAL/CiRCLE")
        # We search globally or in shared drives for this high-level folder
        version_query = (
            f"name contains '{version}' "
            f"and '{root_id}' in parents "
            f"and mimeType = 'application/vnd.google-apps.folder' "
            f"and trashed = false"
        )

        # Execute Search 1
        v_results = (
            self.service.files()
            .list(q=version_query, fields="files(id, name)")
            .execute()
        )

        v_files = v_results.get("files", [])

        if not v_files:
            raise ValueError(f"Version Folder '{version}' not found anywhere.")

        # We assume the first match is the correct one (handling duplicates is harder)
        for v_file in v_files:
            if v_file["name"].split(" ")[1:] == version.split(" "):
                version_id = v_file["id"]
                break
        else:
            raise ValueError(f"Version Folder '{version}' not found anywhere.")

        print(f"Hunting for '{song_name}'")

        # 2. Search for the base name first
        # We use 'contains' instead of 'equals' to find "Song (DX)"
        # I exclude charts which are utage
        query = (
            f"name contains '{song_name}' "
            # f"and not name contains '['" 
            f"and '{version_id}' in parents "
            f"and mimeType = 'application/vnd.google-apps.folder' "
            f"and trashed = false"
        )
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        candidates = results.get("files", [])

        if not candidates:
            raise ValueError(
                f"❌ No folders found matching '{song_name}' inside {version} with id '{version_id}'"
            )

        # 3. Filter Candidates based on Variant
        # logic: exact match vs suffix match

        target_folder = None

        for folder in candidates:
            folder_name = folder["name"]
                
            if variant:
                # Check if folder explicitly says (DX) or (STD)
                # Normalizes to ignore case: "(dx)" == "(DX)"
                if f"({variant})" in folder_name.upper():
                    target_folder = folder
                    break
               
            if song_name == folder_name:
                target_folder = folder
                break

            

        # If we didn't find a specific match in the loop, default to the first candidate
        if not target_folder:
            candidates.sort(key=lambda x: len(x["name"]))
            
            print(
                f"Precise match failed. Defaulting to shortest match: {candidates[0]['name']}"
            )
            target_folder = candidates[0]

        print(f"Target Locked: {target_folder['name']} (ID: {target_folder['id']})")
        return target_folder["id"]

    def download_folder(self, folder_id, local_path):
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        self._recursive_download(folder_id, local_path)

    def _recursive_download(self, parent_id, current_local_path):
        query = f"'{parent_id}' in parents and trashed=false"
        results = (
            self.service.files()
            .list(q=query, fields="files(id, name, mimeType, size)")
            .execute()
        )

        items = results.get("files", [])

        if not items:
            return

        for item in items:
            file_id = item["id"]
            name = item["name"]
            mime_type = item["mimeType"]
            item_path = os.path.join(current_local_path, name)

            if mime_type == "application/vnd.google-apps.folder":
                if not os.path.exists(item_path):
                    os.makedirs(item_path)
                self._recursive_download(file_id, item_path)
            else:
                # Skip if file already exists and size matches (Optimization!)
                if os.path.exists(item_path):
                    local_size = os.path.getsize(item_path)
                    remote_size = int(item.get("size", 0))
                    if local_size == remote_size:
                        print(f"   ⏩ Skipping {name} (Already exists)")
                        continue

                self._download_file(file_id, item_path, name, item.get("size", 0))

    def _download_file(self, file_id, filepath, filename, filesize):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(filepath, "wb")
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        total_size = int(filesize) if filesize else 1024 * 1024
        with tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            desc=f"   ⬇️ {filename}",
            leave=False,
        ) as pbar:
            while done is False:
                status, done = downloader.next_chunk()
                if status:
                    pbar.update(status.resumable_progress - pbar.n)
        fh.close()
