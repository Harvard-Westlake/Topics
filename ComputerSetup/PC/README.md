<div align="center">

# PC Setup
*<font color="#8b949e">Development environment setup for Windows</font>*

<font color="#3fb950">Environment Configuration</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[1. Terminal](#1-terminal)**  
Install WSL and Ubuntu to get a Unix shell on Windows.

**[2. Authenticator App](#2-authenticator-app)**  
Download a two-factor authentication app to your phone.

**[3. GitHub Accounts](#3-github-accounts)**  
Create two GitHub accounts and enable 2FA on both.

**[4. Git](#4-git)**  
Install Git inside Ubuntu.

**[5. GitKraken](#5-gitkraken)**  
Install and sign in to the visual Git client.

**[6. Visual Studio Code](#6-visual-studio-code)**  
Install VS Code and the Java extension pack.

**[7. Java 21 LTS](#7-java-21-lts)**  
Install Java 21 for Windows.

**[8. Verify Your Setup](#8-verify-your-setup)**  
Confirm Git and Java are working end-to-end.

**[9. Update Your GitHub Profile](#9-update-your-github-profile)**  
Add a photo and submit your profile URL.

---

## <font color="#388bfd">1. Terminal</font>

Windows does not come with a Unix shell. This step installs one through **WSL** (Windows Subsystem for Linux) with Ubuntu. Without it, the commands in the Terminal lessons will not work.

> [!NOTE]
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

> [!WARNING]
> Remember this password. Ubuntu will ask for it when you run commands with elevated permissions.

After setup, you will see a prompt like this:

```
yourname@DESKTOP-ABC:~$
```

> [!NOTE]
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

Before creating your GitHub accounts, download an authenticator app on your smartphone. You will need it to set up two-factor authentication.

Choose one of these:

| App | Cost |
|---|---|
| Authy | Free |
| Google Authenticator | Free |
| Microsoft Authenticator | Free |
| Duo Mobile | Free |
| 1Password | Paid |
| LastPass | Paid |

After installing, sign up using your **personal email address**.

---

## <font color="#388bfd">3. GitHub Accounts</font>

You will create **two separate GitHub accounts** — one for school, one personal.

### <font color="#79c0ff">Account 1 — School account</font>

Use your **hwemail.com** address to create the first account.

> [!NOTE]
> Your HW email account has restrictions that may limit some advanced coding activities. This is expected — use your personal account for those.

After creating it, enable **two-factor authentication**:

1. Go to **Settings → Password and Authentication → Two-factor Authentication**
2. Follow the prompts
3. When shown a QR code, scan it with the authenticator app you installed in step 2

### <font color="#79c0ff">Account 2 — Personal account</font>

Use your **personal email address** to create the second account.

> [!NOTE]
> Your personal account will not qualify for the free GitHub Student Developer Pack — that requires your school email.

### <font color="#79c0ff">GitHub Student Developer Pack</font>

Sign up for the [GitHub Student Developer Pack](https://education.github.com/pack) using your **hwemail.com** account. This unlocks free pro access to GitKraken and other tools.

> [!TIP]
> You likely won't need proof of enrollment if you use your hwemail.com address — GitHub recognises school email domains automatically.

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

> [!TIP]
> If `git --version` says "command not found", close the Ubuntu app and reopen it, then try again.

---

## <font color="#388bfd">5. GitKraken</font>

GitKraken is a visual interface for Git that you'll use in class.

1. Download and install GitKraken from [gitkraken.com/download](https://www.gitkraken.com/download)
2. Open GitKraken and sign in using your **hwemail.com** GitHub account — the one registered for the Student Developer Pack

> [!WARNING]
> You will likely see only a **7-day trial** at first. This is normal — your Student Developer Pack application takes time to be approved. Once approved, GitKraken Pro activates automatically. Make sure to click the confirmation email from GitHub to activate your pro features.

---

## <font color="#388bfd">6. Visual Studio Code</font>

1. Download and install VS Code from [code.visualstudio.com/download](https://code.visualstudio.com/download)
2. Open VS Code
3. Open the Extensions panel (`Ctrl + Shift + X`)
4. Search for and install: **Extension Pack for Java**

---

## <font color="#388bfd">7. Java 21 LTS</font>

Go to [Windows Java Downloads — Oracle](https://www.oracle.com/java/technologies/downloads/#jdk21-windows) and download the **x64 Installer**.

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

On your **hwemail.com GitHub account**:

1. Add a profile photo
2. Open your profile in an **incognito window** to confirm it is publicly visible
3. Copy your profile URL — it follows the format:

```
https://github.com/your-username
```

Submit this URL as directed by your teacher.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you open the Ubuntu app on your Windows machine?
- [ ] Can you run `git --version` inside Ubuntu without seeing an error?
- [ ] Can you log in to both of your GitHub accounts in the browser?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you navigate to your Ubuntu home folder from Windows File Explorer using `\\wsl.localhost\Ubuntu\home`?
- [ ] Can you create and run a Java file in VS Code that prints output?
- [ ] Can you open GitKraken and confirm it shows your hwemail.com GitHub account?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain what WSL is and why it was installed?
- [ ] Can you configure Git with your name and email using `git config` inside Ubuntu?
- [ ] Can you clone a public GitHub repository to your machine using the Ubuntu terminal?

---

← Back to [Computer Setup](../)
