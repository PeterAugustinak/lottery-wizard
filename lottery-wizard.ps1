Write-Host INSTALLING ENVIRONMENT

  python -m venv venv
  cd venv/Scripts
  .\activate
  cd ..
  cd ..
  python -m pip install --upgrade pip
  pip install -r requirements.txt

Write-Host STARTING ELECTION MADNESS
  cd src  
  python lottery.py

  cd ..
  cd venv/Scripts
  .\deactivate
  cd ..
  cd ..

