import json
import os
from datetime import datetime


class DataManager:
    def __init__(self):
        self.users_file = 'data/users.json'
        self.projects_file = 'data/projects.json'
        self.groups_file = 'data/groups.json'
        self.friends_file = 'data/friends.json'

        # Utwórz folder data jeśli nie istnieje
        os.makedirs('data', exist_ok=True)

        # Załaduj dane
        self.users = self.load_data(self.users_file)
        self.projects = self.load_data(self.projects_file)
        self.groups = self.load_data(self.groups_file)
        self.friends = self.load_data(self.friends_file)

    def load_data(self, filename):
        """Załaduj dane z pliku JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_data(self, data, filename):
        """Zapisz dane do pliku JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # === UŻYTKOWNICY ===
    def get_user(self, username):
        """Pobierz dane użytkownika"""
        return self.users.get(username)

    def add_user(self, username, user_data):
        """Dodaj nowego użytkownika"""
        user_data['created_at'] = datetime.now().isoformat()
        self.users[username] = user_data
        self.save_data(self.users, self.users_file)

    def validate_user(self, username, password):
        """Sprawdź dane logowania"""
        user = self.get_user(username)
        if user and user.get('password') == password:
            return True
        return False

    def user_exists(self, username):
        """Sprawdź czy użytkownik istnieje"""
        return username in self.users

    # === PROJEKTY ===
    def get_projects_by_user(self, username, project_type='all'):
        """Pobierz projekty użytkownika"""
        user_projects = []
        for project_id, project in self.projects.items():
            if project_type == 'sent' and project.get('author') == username:
                user_projects.append({**project, 'id': project_id})
            elif project_type == 'received' and username in project.get('recipients', []):
                user_projects.append({**project, 'id': project_id})
            elif project_type == 'all':
                if project.get('author') == username or username in project.get('recipients', []):
                    user_projects.append({**project, 'id': project_id})
        return user_projects

    def add_project(self, project_data):
        """Dodaj nowy projekt"""
        project_id = f"proj_{len(self.projects) + 1}_{int(datetime.now().timestamp())}"
        project_data['created_at'] = datetime.now().isoformat()
        project_data['status'] = 'active'
        project_data['offers'] = []

        self.projects[project_id] = project_data
        self.save_data(self.projects, self.projects_file)
        return project_id

    def get_project(self, project_id):
        """Pobierz szczegóły projektu"""
        return self.projects.get(project_id)

    def update_project(self, project_id, updates):
        """Zaktualizuj projekt"""
        if project_id in self.projects:
            self.projects[project_id].update(updates)
            self.save_data(self.projects, self.projects_file)

    def add_offer_to_project(self, project_id, offer_data):
        """Dodaj ofertę do projektu"""
        if project_id in self.projects:
            offer_data['created_at'] = datetime.now().isoformat()
            self.projects[project_id]['offers'].append(offer_data)
            self.save_data(self.projects, self.projects_file)

    # === ZNAJOMI ===
    def get_friends(self, username):
        """Pobierz listę znajomych"""
        return self.friends.get(username, [])

    def add_friend(self, username, friend_username):
        """Dodaj znajomego"""
        if username not in self.friends:
            self.friends[username] = []

        if friend_username not in self.friends[username]:
            self.friends[username].append(friend_username)
            self.save_data(self.friends, self.friends_file)

    def remove_friend(self, username, friend_username):
        """Usuń znajomego"""
        if username in self.friends and friend_username in self.friends[username]:
            self.friends[username].remove(friend_username)
            self.save_data(self.friends, self.friends_file)

    def are_friends(self, username1, username2):
        """Sprawdź czy użytkownicy są znajomymi"""
        friends1 = self.friends.get(username1, [])
        friends2 = self.friends.get(username2, [])
        return username2 in friends1 or username1 in friends2

    # === GRUPY ===
    def get_groups_by_user(self, username, membership_type='member'):
        """Pobierz grupy użytkownika"""
        user_groups = []
        for group_id, group in self.groups.items():
            if membership_type == 'member' and username in group.get('members', []):
                user_groups.append({**group, 'id': group_id})
            elif membership_type == 'owner' and group.get('owner') == username:
                user_groups.append({**group, 'id': group_id})
            elif membership_type == 'all':
                if username in group.get('members', []) or group.get('owner') == username:
                    user_groups.append({**group, 'id': group_id})
        return user_groups

    def get_available_groups(self, username):
        """Pobierz dostępne grupy (nie należy do nich użytkownik)"""
        available_groups = []
        for group_id, group in self.groups.items():
            if username not in group.get('members', []) and group.get('owner') != username:
                if group.get('type') == 'public':
                    available_groups.append({**group, 'id': group_id})
        return available_groups

    def create_group(self, group_data):
        """Utwórz nową grupę"""
        group_id = f"group_{len(self.groups) + 1}_{int(datetime.now().timestamp())}"
        group_data['created_at'] = datetime.now().isoformat()
        group_data['members'] = group_data.get('members', [])

        # Dodaj twórcy do członków
        if group_data.get('owner') not in group_data['members']:
            group_data['members'].append(group_data['owner'])

        self.groups[group_id] = group_data
        self.save_data(self.groups, self.groups_file)
        return group_id

    def join_group(self, group_id, username):
        """Dołącz do grupy"""
        if group_id in self.groups:
            if username not in self.groups[group_id]['members']:
                self.groups[group_id]['members'].append(username)
                self.save_data(self.groups, self.groups_file)

    def leave_group(self, group_id, username):
        """Opuść grupę"""
        if group_id in self.groups:
            if username in self.groups[group_id]['members']:
                self.groups[group_id]['members'].remove(username)
                self.save_data(self.groups, self.groups_file)

    def get_group(self, group_id):
        """Pobierz szczegóły grupy"""
        return self.groups.get(group_id)

    # === STATYSTYKI ===
    def get_user_stats(self, username):
        """Pobierz statystyki użytkownika"""
        sent_projects = self.get_projects_by_user(username, 'sent')
        received_projects = self.get_projects_by_user(username, 'received')
        friends_count = len(self.get_friends(username))
        groups_count = len(self.get_groups_by_user(username))

        completed_projects = [p for p in sent_projects if p.get('status') == 'completed']
        active_projects = [p for p in sent_projects if p.get('status') == 'active']

        return {
            'sent_projects': len(sent_projects),
            'received_projects': len(received_projects),
            'completed_projects': len(completed_projects),
            'active_projects': len(active_projects),
            'friends_count': friends_count,
            'groups_count': groups_count,
            'completion_rate': len(completed_projects) / len(sent_projects) * 100 if sent_projects else 0
        }

    # === WYSZUKIWANIE ===
    def search_users(self, query, exclude_user=None):
        """Wyszukaj użytkowników"""
        results = []
        query = query.lower()

        for username, user_data in self.users.items():
            if exclude_user and username == exclude_user:
                continue

            if (query in username.lower() or
                    query in user_data.get('company', '').lower() or
                    query in user_data.get('specialization', '').lower()):
                results.append({
                    'username': username,
                    **user_data
                })

        return results

    def search_projects(self, query, username=None):
        """Wyszukaj projekty"""
        results = []
        query = query.lower()

        for project_id, project in self.projects.items():
            if (query in project.get('name', '').lower() or
                    query in project.get('description', '').lower() or
                    query in project.get('location', '').lower()):

                # Jeśli podano username, filtruj tylko projekty dostępne dla tego użytkownika
                if username:
                    if project.get('author') == username or username in project.get('recipients', []):
                        results.append({**project, 'id': project_id})
                else:
                    results.append({**project, 'id': project_id})

        return results