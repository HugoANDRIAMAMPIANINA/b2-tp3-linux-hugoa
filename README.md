# TP3 : Développement d'un outil pour les admins

# Outil de monitoring

## Installation

Installation et lancement du script init pour créer le user, les dossiers et lancer le service
```bash
git clone https://github.com/HugoANDRIAMAMPIANINA/b2-tp3-linux-hugoa
cd b2-tp3-linux-hugoa/
chmod +x init.sh
sudo ./init.sh
```

## Usage

- Lancer un check des ressources du système dont la RAM, le disque, le CPU et l'état des ports TCP précisés dans le fichier de conf `monit.conf` et afficher ces valeurs dans le terminal. Stock les valeurs dans un fichier `json` dans `/var/monit` :
    ```bash
    sudo -u monit-man monit.py --check
    ```
- Afficher la liste des rapports qui ont été effectués :
    ```bash
    sudo -u monit-man monit.py --list
    ```
- Afficher le dernier rapport :
    ```bash
    sudo -u monit-man monit.py --get-last
    ```
- Afficher les valeurs moyennes des X dernières heures selon les rapports :
    ```bash
    sudo -u monit-man monit.py --get-avg X
    ```

## Configuration

Fichier de configuration : [monit.conf](/conf/monit.conf)

Il se situe dans `/etc/monit/monit.conf`

### Structure :

```json
{
    "tcp_ports": []
}
```

Pour ajouter des ports à surveiller,  : 

```json
# chaque port doit être séparé par une virgule
{
    "tcp_ports": [80,443,22,8888]
}
```