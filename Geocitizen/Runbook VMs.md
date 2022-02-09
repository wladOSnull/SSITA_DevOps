# Virtualization

## Main

- CentOS 7.9.2004
https://www.osboxes.org/centos/

- Ubuntu 20.04.3 Focal Fossa
https://www.osboxes.org/ubuntu/  

Download these .vdi files and create new VMs, there is small tutorial also:

- Installing / using .vdi file Oracle VM VirtualBox
https://www.youtube.com/watch?v=VDh9Re_s6c8

### In VirtuaBox

For each VMs:
- ROM 2GB
- .vdi images from https://www.osboxes.org/

Settings:
- General->Advanced: Shared clipboard and Drag'n'Drop - Bidirectional
- System->Motherboard: ROM 2GB; Boot order (Optical, Hard, Network)
- System->Processor: 2CPU
- Display: Video Memory 128MB (max)
- Network: Bridget Adapter
- Shared folder: create new and select it

**Start Ubuntu ... fix it ... start CentOS ... fix it ... migrate CentOS into Rocky ... done ?**

## Ubuntu fix

- Guest addition (drag&drop AND shared folder !) + GUI and GUI-less
https://www.itzgeek.com/post/how-to-install-virtualbox-guest-additions-on-ubuntu-20-04/

- For sync folder if you dont want to interact with sudo pass each time
https://www.youtube.com/watch?v=u2Ha0peg9V4

- make accessible via ssh
https://linuxize.com/post/how-to-enable-ssh-on-ubuntu-18-04/

## CentOS fix

- Solving problem with internet connection on CenOS7
https://www.youtube.com/watch?v=PlfxwKHY82M

- Guest additions of VirtualBox for CentOS7
https://linuxconfig.org/how-to-install-virtualbox-guest-additions-on-centos-7-linux

  - If there is problem on '$ ls -l /usr/src/kernels/$(uname -r)' stage from previous guide 
  https://unix.stackexchange.com/questions/232147/your-kernel-headers-for-kernel-3-10-0-229-el7-x86-64-cannot-be-found
  
  ```bash
  ~ sudo yum install "kernel-devel-uname-r == $(uname -r)"
  ```

- For sync folder if you dont want to interact with sudo pass each time
  
  ```bash
  ~ sudo chmod -R 755 /media/<your-sync-folder>/
  ~ sudo usermod -G vboxsf -a osboxes 
  # REBOOT !
  ```

- make accessible via ssh (openssh-server may be installed already !!!)
https://linuxstoney.com/enable-ssh-service-on-rocky-linux-8-centos-8/

## Rocky migration

- Video guide with elevate-leapp
https://www.youtube.com/watch?v=hzywOvhWS_0

- make accessible via ssh (openssh-server may be installed already !!!)
https://linuxstoney.com/enable-ssh-service-on-rocky-linux-8-centos-8/

### Rocky fix (if Guest additions was not installed on CentOS previously)

- Guest additions of VirtualBox for Rocky8
https://www.how2shout.com/linux/two-ways-to-install-virtualbox-guest-addtions-on-rocky-linux-8/

## Appendix

- screenfetch for Rocky
https://tanmaync.wordpress.com/2017/10/02/install-screenfetch-centos7-rhel7/

- logs of ALL connection to the machine
  ```bash
  ~ less /var/log/auth.log
  ```

- Guest Additions for GUI-less
  - choose RIGHT version of VMBox on http://download.virtualbox.org/virtualbox/ 
  
  ```bash
  # downloading Guest Additions via 'wget'
  ~ wget http://download.virtualbox.org/virtualbox/6.1.32/VBoxGuestAdditions_6.1.32.iso

  # creating new folder for mounting .iso with Guest Additions
  ~ sudo mkdir /media/GuestAdditionsISO

  # mounting
  ~ sudo mount -o loop path/to/VBoxGuestAdditions.iso /media/GuestAdditionsISO
  
  # checking files
  ~ cd /media/GuestAdditionsISO
  ~ ls -la

  # installing Guest Additions for Linux type system
  ~ sudo ./VBoxLinuxAdditions.run

  # !!! REQUIRED reboot after './VBoxLinuxAdditions.run' finish installation 
  ~ sudo shutdown now
  ```