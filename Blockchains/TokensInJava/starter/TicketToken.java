import java.util.HashMap;
import java.util.Scanner;

// A complete token in plain Java: a ledger of balances, a mint method, and a
// transfer method with a balance check. Every cryptocurrency you will read or
// write later in this module (including the real ERC20 contract) is this same
// program wearing different syntax. Run it, personalize it, and be ready to
// explain transfer and giveTickets to a classmate, line by line.
public class TicketToken {
    // === YOUR TICKET TOKEN DETAILS ===
    private final String tokenName;                     // You can name your tickets anything
    private final HashMap<String, Long> balances;       // Person's name -> how many tickets they own
    private long totalSupply;                           // Total tickets created so far

    public TicketToken(String ticketName, long initialSupply, String creatorName) {
        this.tokenName = ticketName;
        this.balances = new HashMap<>();
        this.totalSupply = initialSupply;
        balances.put(creatorName, initialSupply);       // Creator gets all initial tickets
        System.out.println("OK: " + tokenName + " created! Total supply: " + totalSupply);
    }

    // Give (mint) new tickets to anyone. Minting creates tickets out of thin
    // air, so the total supply grows - just like a block reward minting coins.
    public void giveTickets(String recipientName, long ticketAmount) {
        if (ticketAmount <= 0) {
            System.out.println("REJECTED: Amount must be positive!");
            return;
        }
        balances.put(recipientName, balances.getOrDefault(recipientName, 0L) + ticketAmount);
        totalSupply += ticketAmount;
        System.out.println("OK: Gave " + ticketAmount + " " + tokenName + " to " + recipientName);
    }

    // Anyone can transfer their own tickets to someone else. Transferring
    // moves existing tickets between balances, so the total supply is
    // unchanged - and the balance check is what makes overspending impossible.
    public void transfer(String senderName, String recipientName, long ticketAmount) {
        long senderBalance = balances.getOrDefault(senderName, 0L);
        if (ticketAmount <= 0) {
            System.out.println("REJECTED: Amount must be positive!");
            return;
        }
        if (senderBalance < ticketAmount) {
            System.out.println("REJECTED: " + senderName + " only has " + senderBalance + " tickets!");
            return;
        }
        balances.put(senderName, senderBalance - ticketAmount);
        balances.put(recipientName, balances.getOrDefault(recipientName, 0L) + ticketAmount);
        System.out.println("OK: " + senderName + " transferred " + ticketAmount
                + " " + tokenName + " to " + recipientName);
    }

    // Check anyone's balance. Balances are public here, exactly as they are
    // on a real blockchain.
    public void checkBalance(String personName) {
        long balance = balances.getOrDefault(personName, 0L);
        System.out.println(personName + "'s balance: " + balance + " " + tokenName);
    }

    // Print all balances (for testing).
    public void printAllBalances() {
        System.out.println("\n=== ALL " + tokenName + " BALANCES ===");
        for (String personName : balances.keySet()) {
            System.out.println(personName + ": " + balances.get(personName));
        }
        System.out.println("Total supply: " + totalSupply);
    }

    public static void main(String[] commandLineArguments) {
        Scanner scanner = new Scanner(System.in);

        // === CHANGE THESE TO MAKE IT YOURS ===
        String ticketName = "ClassTickets";             // Name your tickets whatever you like!
        String creatorName = "YourNameHere";            // Put your own name

        TicketToken tickets = new TicketToken(ticketName, 1000, creatorName);

        // Give some tickets to classmates at the start
        // === CHANGE THESE to your real classmates and your own amounts ===
        tickets.giveTickets("Alice", 150);
        tickets.giveTickets("Bob", 80);
        tickets.giveTickets("Charlie", 50);

        while (true) {
            System.out.println("\n=== " + ticketName + " MENU ===");
            System.out.println("1. Check balance");
            System.out.println("2. Transfer tickets to someone");
            System.out.println("3. Give (mint) new tickets (admin only)");
            System.out.println("4. Show all balances");
            System.out.println("5. Exit");
            System.out.print("Choose an option: ");

            int menuChoice = scanner.nextInt();
            scanner.nextLine(); // consume the leftover newline

            if (menuChoice == 1) {
                System.out.print("Enter person's name: ");
                String personName = scanner.nextLine();
                tickets.checkBalance(personName);
            } else if (menuChoice == 2) {
                System.out.print("Your name (sender): ");
                String senderName = scanner.nextLine();
                System.out.print("Recipient name: ");
                String recipientName = scanner.nextLine();
                System.out.print("Amount to transfer: ");
                long ticketAmount = scanner.nextLong();
                scanner.nextLine();
                tickets.transfer(senderName, recipientName, ticketAmount);
            } else if (menuChoice == 3) {
                System.out.print("Recipient name: ");
                String recipientName = scanner.nextLine();
                System.out.print("Amount to give: ");
                long ticketAmount = scanner.nextLong();
                scanner.nextLine();
                tickets.giveTickets(recipientName, ticketAmount);
            } else if (menuChoice == 4) {
                tickets.printAllBalances();
            } else if (menuChoice == 5) {
                System.out.println("Goodbye!");
                break;
            } else {
                System.out.println("Invalid option.");
            }
        }
        scanner.close();
    }
}
