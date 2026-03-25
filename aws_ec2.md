You can deploy this project on an AWS EC2 instance using the **AWS Free Tier**, which gives you a `t2.micro` or `t3.micro` instance (1 vCPU, 1 GB RAM) free for 12 months. 

However, before we start, **here is a critical warning**: 
> [!WARNING]
> Your application uses the local `all-mpnet-base-v2` embedding model. This model alone requires about 500-600MB of RAM. When combined with FastAPI, Streamlit, and processing PDFs, **it will easily exceed the 1 GB RAM limit of a free EC2 instance**, causing the server to crash (Out of Memory).
> 
> **The Fix:** I have included a crucial step below (Step 4) to **add Swap Space**. This uses your hard drive as "fake RAM". It will make the app slightly slower, but it will prevent it from crashing on the free tier!

Here is the step-by-step guide to deploying it for free:

### Step 1: Launch the EC2 Instance
1. Log into the AWS Console and go to **EC2 > Instances > Launch instances**.
2. **Name**: `rag-qa-deployment`
3. **OS Image (AMI)**: Select **Ubuntu** (Ubuntu Server 24.04 LTS is fine).
4. **Instance Type**: `t2.micro` or `t3.micro` (Must say "Free tier eligible").
5. **Key Pair**: Create a new key pair (e.g., `rag-key.pem`) and download it to your computer.
6. **Network Settings**: Check the boxes for:
   - Allow SSH traffic from Anywhere
   - Allow HTTP traffic from the internet
7. Click **Launch Instance**.

### Step 2: Open Required Ports (Security Group)
Your FastAPI runs on `8000` and Streamlit on `8501`. We need to open these ports to the internet.
1. In the EC2 Dashboard, click your running instance.
2. Select the **Security** tab and click on the **Security group** link.
3. Click **Edit inbound rules** -> **Add Rule**:
   - **Type**: Custom TCP
   - **Port range**: `8000`
   - **Source**: `0.0.0.0/0`
4. Click **Add Rule** again:
   - **Type**: Custom TCP
   - **Port range**: `8501`
   - **Source**: `0.0.0.0/0`
5. Save the rules.

### Step 3: Connect to the Instance
Open Windows PowerShell, navigate to where you downloaded your `.pem` key, and SSH into your instance:
```powershell
ssh -i "rag-key.pem" ubuntu@<YOUR_EC2_PUBLIC_IP>
```

### Step 4: Prevent Crashes (Add Swap Space)
Once logged into your EC2 terminal, run these commands exactly to add 2GB of Swap Space so your embedding model doesn't crash the server:
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo cp /etc/fstab /etc/fstab.bak
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Step 5: Transfer Your Files & Prepare Environment
The easiest way to get your code onto the server is to push it to a private GitHub repository, and then `git clone` it on the server. Alternatively, use SCP.

Once your code is on the server (`/home/ubuntu/rag_qa_system`), change the `BACKEND_URL` in [frontend/app.py](cci:7://file:///C:/2026%20AI%20Projects/rag_qa_system/frontend/app.py:0:0-0:0):
Change `BACKEND_URL = "http://127.0.0.1:8000"` to your EC2's Public IP: 
`BACKEND_URL = "http://<YOUR_EC2_PUBLIC_IP>:8000"`

Then, set up Python:
```bash
sudo apt update
sudo apt install python3.12-venv python3-pip -y
cd rag_qa_system
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 6: Keep the App Running Forever
If you just run the commands normally, they will shut down when you close your PowerShell window. We will use `tmux` (or `nohup`) to keep them running in the background forever.

1. Open a new tmux session: `tmux new -s rag`
2. Start the backend:
   ```bash
   source .venv/bin/activate
   uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```
3. Press `Ctrl+B`, then release both and press `C` to open a new tab in tmux.
4. Start the frontend:
   ```bash
   source .venv/bin/activate
   streamlit run frontend/app.py
   ```
5. You can now leave tmux by pressing `Ctrl+B`, then release and press `D` (Detach). You can safely close PowerShell.

You can now visit your live app at `http://<YOUR_EC2_PUBLIC_IP>:8501`!