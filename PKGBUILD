pkgname=enlog
pkgdesc="Gathers selected system logs and generates a sharable link."
url="https://github.com/andanotherusername/enlog.git"
pkgver=0.1
pkgrel=1

arch=("any")
license=("GPL")
depends=(python-pycurl python-pyperclip python-pyqt5)

source=("enlog::git+$url#branch=master")

sha256sums=(SKIP)

package(){
    cd $srcdir/$pkgname
    python setup.py install --root=$pkgdir
    install -d $pkgdir/usr/share/applications
    install -Dm755 $pkgname.desktop         $pkgdir/usr/share/applications/$pkgname.desktop
}
