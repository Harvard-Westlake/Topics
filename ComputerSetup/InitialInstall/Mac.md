<div align="center">

# Mac Setup
*<font color="#8b949e">Development environment setup for macOS</font>*

<font color="#3fb950">Environment Configuration</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[1. Terminal](#1-terminal)**  
Open the built-in macOS terminal and confirm your Unix shell is working.

**[2. Authenticator App](#2-authenticator-app)**  
Download a two-factor authentication app to your phone.

**[3. GitHub Accounts](#3-github-accounts)**  
Create two GitHub accounts and enable 2FA on both.

**[4. Homebrew](#4-homebrew)**  
Install the macOS package manager used to install Git and other tools.

**[5. Git](#5-git)**  
Install Git via Homebrew.

**[6. GitKraken](#6-gitkraken)**  
Install and sign in to the visual Git client.

**[7. Visual Studio Code](#7-visual-studio-code)**  
Install VS Code and the Java extension pack.

**[8. Java 21 LTS](#8-java-21-lts)**  
Check your chip type and install the correct Java version.

**[9. Verify Your Setup](#9-verify-your-setup)**  
Confirm Git and Java are working end-to-end.

**[10. Update Your GitHub Profile](#10-update-your-github-profile)**  
Add a photo and submit your profile URL.

---

## <font color="#388bfd">1. Terminal</font>

macOS comes with Terminal built in. No installation required.

Open it with Spotlight: press **Cmd + Space**, type `Terminal`, and press Return.

You will see a prompt like this:

```
yourname@MacBook-Air ~ %
```

> **Note:**
> The `%` means your shell is **zsh** — macOS's default since Catalina (2019). All Terminal lessons in this course use zsh. If your prompt ends with `$` instead, run `chsh -s /bin/zsh` and restart Terminal.

Your Unix terminal is ready. The remaining steps install the tools you will use with it.

---

## <font color="#388bfd">2. Authenticator App</font>

Before creating your GitHub accounts, download an authenticator app on your smartphone. You will need it to set up two-factor authentication.

Choose one of these:

| App | Cost |
|---|---|
| Authy | Free |
| Google Authenticator | Free |
| Microsoft Authenticator | Free |
| Passwords *(Apple — iOS 18 only)* | Free |
| Duo Mobile | Free |
| 1Password | Paid |
| LastPass | Paid |

After installing, sign up using your **personal email address**.

---

## <font color="#388bfd">3. GitHub Accounts</font>

You will create **two separate GitHub accounts** — one for school, one personal.

### <font color="#79c0ff">Account 1 — School account</font>

Use your **hwemail.com** address to create the first account.

> **Note:**
> Your HW email account has restrictions that may limit some advanced coding activities. This is expected — use your personal account for those.

After creating it, enable **two-factor authentication**:

1. Go to **Settings → Password and Authentication → Two-factor Authentication**
2. Follow the prompts
3. When shown a QR code, scan it with the authenticator app you installed in step 2

### <font color="#79c0ff">Account 2 — Personal account</font>

Use your **personal email address** to create the second account.

> **Note:**
> Your personal account will not qualify for the free GitHub Student Developer Pack — that requires your school email.

### <font color="#79c0ff">GitHub Student Developer Pack</font>

Sign up for the [GitHub Student Developer Pack](https://education.github.com/pack) using your **hwemail.com** account. This unlocks free pro access to GitKraken and other tools.

> **Tip:**
> You likely won't need proof of enrollment if you use your hwemail.com address — GitHub recognises school email domains automatically.

---

## <font color="#388bfd">4. Homebrew</font>

Homebrew is a package manager for macOS that makes installing developer tools straightforward.

Open **Terminal** and paste the command from the [Homebrew installation page](https://brew.sh/). It will look something like:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the prompts. Homebrew may install Xcode Command Line Tools first — allow it.

---

## <font color="#388bfd">5. Git</font>

Once Homebrew is installed, install Git:

```bash
brew install git
```

Verify it worked:

```bash
git --version
# git version 2.x.x
```

> **Tip:**
> If `git --version` says "command not found", close Terminal and reopen it, then try again.

---

## <font color="#388bfd">6. GitKraken</font>

GitKraken is a visual interface for Git that you'll use in class.

1. Download and install GitKraken from [gitkraken.com/download](https://www.gitkraken.com/download)
2. Open GitKraken and sign in using your **hwemail.com** GitHub account — the one registered for the Student Developer Pack

> **Warning:**
> You will likely see only a **7-day trial** at first. This is normal — your Student Developer Pack application takes time to be approved. Once approved, GitKraken Pro activates automatically. Make sure to click the confirmation email from GitHub to activate your pro features.

---

## <font color="#388bfd">7. Visual Studio Code</font>

1. Download and install VS Code from [code.visualstudio.com/download](https://code.visualstudio.com/download)
2. Open VS Code
3. Open the Extensions panel (`Cmd + Shift + X`)
4. Search for and install: **Extension Pack for Java**

---

## <font color="#388bfd">8. Java 21 LTS</font>

### <font color="#79c0ff">Check your chip type first</font>

macOS runs on two different chip architectures and you must download the matching Java installer.

1. Click the **Apple menu** (top-left corner of your screen)
2. Select **About This Mac**
3. Look at the **Chip** or **Processor** field:

| What it says | Your chip |
|---|---|
| Apple M1, M2, M3, M4… | M-chip (Apple Silicon) |
| Intel Core i5, i7, i9… | Intel |

### <font color="#79c0ff">Download Java 21 LTS</font>

Go to [Mac Java Downloads — Oracle](https://www.oracle.com/java/technologies/downloads/#jdk21-mac) and download the right installer:

| Chip | Installer to download |
|---|---|
| Intel Mac | **x64 DMG Installer** |
| M-chip Mac | **ARM64 DMG Installer** |

Open the `.dmg` file and follow the installation prompts.

---

## <font color="#388bfd">9. Verify Your Setup</font>

### <font color="#79c0ff">Confirm your terminal environment</font>

Open Terminal and check the three core tools:

```bash
git --version
# git version 2.x.x

java -version
# java version "21.x.x"

brew --version
# Homebrew x.x.x
```

All three should print version numbers, not errors.

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

## <font color="#388bfd">10. Update Your GitHub Profile</font>

On your **hwemail.com GitHub account**:

1. Add a profile photo
2. Open your profile in an **incognito window** to confirm it is publicly visible
3. Copy your profile URL — it follows the format:

```
https://github.com/your-username
```

Submit this URL as directed by your teacher.

---

← Back to [Initial Install](README.md)
