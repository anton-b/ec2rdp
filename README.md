# EC2RDP

A Python command-line tool for managing AWS EC2 instances and connecting to Windows instances via Remote Desktop Protocol (RDP).

## Features

- List all EC2 instances in your AWS account
- Start and stop EC2 instances
- Connect to Windows EC2 instances via RDP using Remmina
- Automatically stop instances after RDP connection (optional)
- AWS credential verification
- Color-coded terminal output for better readability

## Prerequisites

- Python 3.x
- AWS account with appropriate EC2 permissions
- Remmina (for RDP connections) - Install with: `sudo apt-get install remmina` (Ubuntu/Debian)
- AWS credentials configured

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ec2rdp
   ```

2. Set up the environment and install dependencies:
   ```bash
   make install
   ```

3. Activate the virtual environment:
   ```bash
   . venv/bin/activate
   ```

4. Configure AWS credentials:
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your AWS credentials:
   ```
   AWS_ACCESS_KEY_ID=your_access_key_id
   AWS_SECRET_ACCESS_KEY=your_secret_access_key
   AWS_DEFAULT_REGION=us-east-1
   ```

## Usage

The main script is `ec2rdp` which provides several commands for managing EC2 instances.

### List all EC2 instances
```bash
./ec2rdp --list-instances
```

### Start an EC2 instance
```bash
./ec2rdp --start-instance i-1234567890abcdef0
```

### Stop an EC2 instance
```bash
./ec2rdp --stop-instance i-1234567890abcdef0
```

### Connect to an instance via RDP
```bash
./ec2rdp --connect-rdp i-1234567890abcdef0
```

### Connect via RDP with custom username
```bash
./ec2rdp --connect-rdp i-1234567890abcdef0 --username MyUser
```

### Connect via RDP and auto-stop the instance after disconnection
```bash
./ec2rdp --connect-rdp i-1234567890abcdef0 --autostop
```

### Connect via RDP, auto-stop, but don't wait for the instance to stop
```bash
./ec2rdp --connect-rdp i-1234567890abcdef0 --autostop --nowait
```

## Command Line Options

- `--list-instances`: List all EC2 instances
- `--start-instance <instance-id>`: Start a specific EC2 instance by ID
- `--stop-instance <instance-id>`: Stop a specific EC2 instance
- `--connect-rdp <instance-id>`: Connect to an EC2 instance via RDP
- `--username <username>`: RDP username (default: Administrator)
- `--autostop`: Automatically stop instances after connecting via RDP
- `--nowait`: Do not wait for instance to stop after stopping it

## Makefile Commands

- `make install`: Set up virtual environment and install dependencies
- `make clean`: Remove the virtual environment

## Dependencies

- `boto3`: AWS SDK for Python
- `python-dotenv`: Load environment variables from .env file

## Notes

- The tool automatically starts instances before attempting RDP connections
- RDP connections use Remmina as the client
- All AWS operations require valid credentials and appropriate IAM permissions
- The tool provides color-coded output (green for success, red for errors, yellow for warnings, blue for information)

## Troubleshooting

1. **Invalid AWS credentials**: Ensure your `.env` file contains valid AWS credentials
2. **No public IP**: Make sure your EC2 instance has a public IP address for RDP connections
3. **Remmina not found**: Install Remmina using your system's package manager
4. **Permission denied**: Ensure your AWS user has the necessary EC2 permissions (ec2:DescribeInstances, ec2:StartInstances, ec2:StopInstances, etc.)