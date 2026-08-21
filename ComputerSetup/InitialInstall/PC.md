<div align="center">

# PC Setup
*<font color="#8b949e">Development environment setup for Windows</font>*

<font color="#3fb950">Environment Configuration</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

1. [Install WSL and Ubuntu to get a Unix shell on Windows](#1-terminal)
2. [Download an authenticator app for two-factor authentication](#2-authenticator-app)
3. [Create your GitHub account and enable two-factor authentication](#3-github-account)
4. [Install Git inside Ubuntu](#4-git)
5. [Install GitKraken and sign in with your GitHub account](#5-gitkraken)
6. [Install VS Code and the Java extension pack](#6-visual-studio-code)
7. [Install Java 25 LTS for Windows](#7-java-25-lts)
8. [Verify that Git and Java both work](#8-verify-your-setup)
9. [Add a photo and submit your GitHub profile URL](#9-update-your-github-profile)

---

## <font color="#388bfd">1. Terminal</font>

Windows does not come with a Unix shell. This step installs one through **WSL** (Windows Subsystem for Linux) with Ubuntu. Without it, the commands in the Terminal lessons will not work.

> **Note:**
> This step requires two restarts and takes about 15 minutes. You will only do it once.

### <font color="#79c0ff">Step 1 — Enable Virtual Machine Platform</font>

1. In the Windows search bar, type **"Turn Windows features on or off"** and open it
2. Check the box for **Virtual Machine Platform**
3. Click OK and **restart your computer** when prompted

### <font color="#79c0ff">Step 2 — Install Ubuntu from the Microsoft Store</font>

Open the Microsoft Store and install **Ubuntu 20.04.6 LTS**.

### <font color="#79c0ff">Step 3 — Run WSL install</font>

Open **PowerShell** or **Command Prompt** and run:

```bash
wsl --install
```

**Restart your computer** once more when it completes.

### <font color="#79c0ff">Step 4 — Set up your Ubuntu username and password</font>

Launch the **Ubuntu** app from the Start menu. Follow the prompts to create a username and password.

> **Warning:**
> Remember this password. Ubuntu will ask for it when you run commands with elevated permissions.

After setup, you will see a prompt like this:

```
yourname@DESKTOP-ABC:~$
```

> **Note:**
> The `$` means you are running **bash** inside Ubuntu. All Unix commands work the same way here as they do in Terminal on a Mac. From now on, whenever this course says "open the terminal," use the Ubuntu app — not PowerShell or Command Prompt.

### <font color="#79c0ff">Accessing your Ubuntu files from Windows</font>

To browse your Ubuntu files in File Explorer, enter one of these paths in the address bar:

```
\\wsl$
```

For direct access to your Ubuntu home folder:

```
\\wsl.localhost\Ubuntu\home
```

You should see a single folder named after your Ubuntu username.

---

## <font color="#388bfd">2. Authenticator App</font>

Before creating your GitHub account, download an authenticator app on your smartphone. You will need it to set up two-factor authentication.

Choose one of these free options:

- Authy
- Google Authenticator
- Microsoft Authenticator
- Duo Mobile

After installing, sign up using your **personal email address**.

---

## <font color="#388bfd">3. GitHub Account</font>

Create a GitHub account using your **personal email address** — this is the account you will use for the rest of the course.

After creating it, enable **two-factor authentication**:

1. Go to **Settings → Password and Authentication → Two-factor Authentication**
2. Follow the prompts
3. When shown a QR code, scan it with the authenticator app you installed in step 2

---

## <font color="#388bfd">4. Git</font>

Open the **Ubuntu app** and install Git:

```bash
sudo apt update && sudo apt install git -y
```

Verify it worked:

```bash
git --version
# git version 2.x.x
```

> **Tip:**
> If `git --version` says "command not found", close the Ubuntu app and reopen it, then try again.

---

## <font color="#388bfd">5. GitKraken</font>

GitKraken is a visual interface for Git that you'll use in class.

1. Download and install GitKraken from [gitkraken.com/download](https://www.gitkraken.com/download)
2. Open GitKraken and sign in with the GitHub account you just created

> **Note:**
> Sign up for the **Free** plan — do not start a paid trial or enter any payment information. Everything in this course works on the free plan.

---

## <font color="#388bfd">6. Visual Studio Code</font>

1. Download and install VS Code from [code.visualstudio.com/download](https://code.visualstudio.com/download)
2. Open VS Code
3. Open the Extensions panel (`Ctrl + Shift + X`)
4. Search `java` and install: **Extension Pack for Java**

![VS Code Extensions panel with "java" searched in the marketplace; an arrow marked 1 points from the Extensions icon in the sidebar to an arrow marked 2 pointing at the Install button next to "Extension Pack for Java"](assets/vscode-extension-pack-for-java.png)

---

## <font color="#388bfd">7. Java 25 LTS</font>

Go to [Windows Java Downloads — Oracle](https://www.oracle.com/java/technologies/downloads/#jdk25-windows) and download the **x64 Installer**.

Run the installer and follow the prompts.

---

## <font color="#388bfd">8. Verify Your Setup</font>

### <font color="#79c0ff">Confirm your terminal environment</font>

Open the **Ubuntu app** and check the core tools:

```bash
git --version
# git version 2.x.x
```

You should see a version number, not an error.

### <font color="#79c0ff">Run a Java program in VS Code</font>

1. Open VS Code
2. Create a new file called `Hello.java`
3. Paste this code:

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Setup complete!");
    }
}
```

4. Click **Run** (or press `F5`)
5. The VS Code terminal should print: `Setup complete!`

Take a screenshot of the output — you may need to submit it.

---

## <font color="#388bfd">9. Update Your GitHub Profile</font>

On your GitHub account:

1. Add a profile photo
2. Open your profile in an **incognito window** to confirm it is publicly visible
3. Copy your profile URL — it follows the format:

```
https://github.com/your-username
```

Submit this URL as directed by your teacher.

---

← Back to [Initial Install](README.md)
