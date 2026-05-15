<?php

class CTFCodec {

    private string $key;

    // -----------------------------------------------------
    // Constructeur : on dérive la clé en SHA256 (32 octets)
    // -----------------------------------------------------
    public function __construct(string $key) {
        $this->key = hash("sha256", $key, true);
    }

    // -----------------------------------------------------
    // Rotation gauche sur 8 bits
    // -----------------------------------------------------
    private function rotl(int $b, int $n): int {
        return (($b << $n) & 0xFF) | ($b >> (8 - $n));
    }

    // -----------------------------------------------------
    // Rotation droite sur 8 bits
    // -----------------------------------------------------
    private function rotr(int $b, int $n): int {
        return (($b >> $n) | ($b << (8 - $n))) & 0xFF;
    }

    // -----------------------------------------------------
    // Masque pseudo-aléatoire dépendant clé + seed + index
    // -----------------------------------------------------
    private function mask(int $i, int $seed): int {
        $h = hash("sha256", $this->key . chr($seed) . pack("N", $i), true);
        return ord($h[$i % 32]);
    }

    // -----------------------------------------------------
    // Layer 1 : XOR + rotations
    // -----------------------------------------------------
    private function L1E(string $data, int $seed): string {
        $out = "";
        foreach (str_split($data) as $i => $c) {
            $b = ord($c);
            $b = $this->rotl($b, ($i + $seed) % 7);
            $b ^= $this->mask($i, $seed);
            $b = $this->rotr($b, ($seed + $i) % 5);
            $out .= chr($b);
        }
        return $out;
    }

    private function L1D(string $data, int $seed): string {
        $out = "";
        foreach (str_split($data) as $i => $c) {
            $b = ord($c);
            $b = $this->rotl($b, ($seed + $i) % 5);
            $b ^= $this->mask($i, $seed);
            $b = $this->rotr($b, ($i + $seed) % 7);
            $out .= chr($b);
        }
        return $out;
    }

    // -----------------------------------------------------
    // Layer 2 : shuffle pseudo-chaotique (inversible)
    // -----------------------------------------------------
    private function L2E(string $data, int $seed): string {
        $a = str_split($data);
        $n = count($a);

        for ($i = 0; $i < $n; $i++) {
            $j = ($this->mask($i, $seed) + $seed) % $n;
            [$a[$i], $a[$j]] = [$a[$j], $a[$i]];
        }

        return implode("", $a);
    }

    private function L2D(string $data, int $seed): string {
        $a = str_split($data);
        $n = count($a);

        for ($i = $n - 1; $i >= 0; $i--) {
            $j = ($this->mask($i, $seed) + $seed) % $n;
            [$a[$i], $a[$j]] = [$a[$j], $a[$i]];
        }

        return implode("", $a);
    }

    // -----------------------------------------------------
    // Encodage final : Base64URL stable
    // -----------------------------------------------------
    private function b64u_encode(string $d): string {
        return rtrim(strtr(base64_encode($d), "+/", "-_"), "=");
    }

    private function b64u_decode(string $d): string {
        $pad = 4 - (strlen($d) % 4);
        if ($pad < 4) $d .= str_repeat("=", $pad);
        return base64_decode(strtr($d, "-_", "+/"));
    }

    // -----------------------------------------------------
    // ENCODE
    // -----------------------------------------------------
    public function encode(string $msg): string {
        $seed = random_int(0, 255); // seed mutation
        $msg = $this->L1E($msg, $seed);
        $msg = $this->L2E($msg, $seed);
        $msg = $this->b64u_encode($msg);
        return sprintf("%02X", $seed) . "." . $msg;
    }

    // -----------------------------------------------------
    // DECODE
    // -----------------------------------------------------
    public function decode(string $cipher): string {
        if (!strpos($cipher, '.')) return "Erreur: Format invalide.";
        list($hex, $data) = explode(".", $cipher, 2);
        $seed = hexdec($hex);
        $data = $this->b64u_decode($data);
        $data = $this->L2D($data, $seed);
        $data = $this->L1D($data, $seed);
        return $data;
    }
}

/***********************************************
 * ZONE DE DECHIFFREMENT DU MESSAGE INTERCEPTE *
 ***********************************************/

// 1. Entrez la clé de chiffrement
$cle_secrete = ""; 

// 2. Entrez le message chiffré intercepté
$message_intercepte = "";

if ($cle_secrete !== "" && $message_intercepte !== "") {
    $codec = new CTFCodec($cle_secrete);
    $message_clair = $codec->decode($message_intercepte);
    
    echo "========================================\n";
    echo "Clé utilisée    : " . $cle_secrete . "\n";
    echo "Message chiffré : " . $message_intercepte . "\n";
    echo "Message décodé  : " . $message_clair . "\n";
    echo "========================================\n";
} else {
    echo "En attente : Veuillez renseigner la variable \$cle_secrete et la variable \$message_intercepte.\n";
}

?>