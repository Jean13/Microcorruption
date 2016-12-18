def swpb(w)
  return (w & 0xff) << 8 | (w & 0xff00) >> 8
end

0x0001.upto(0xffff) do |w1|
  0x0001.upto(0xffff) do |w2|
    r4 = w1
    r6 = swpb(w1)
    r4 = (r4 + w2) & 0xffff
    r4 = swpb(r4)
    r6 ^= w2
    r6 ^= r4
    r4 ^= r6
    r6 ^= r4

    w3 = r6 ^ 0xfeb1
    if (r4 + w3) & 0xffff == 0x9892
      puts "sol: %04x%04x%04x" % [swpb(w1), swpb(w2), swpb(w3)]
    end
  end
end
